"""Report the three betting slots through the shared Pushover skill."""

import argparse
from datetime import datetime
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SENDER = Path.home() / '.agents/skills/pushover/scripts/send_pushover.py'
ZONE = ZoneInfo('Europe/Stockholm')


def message_for(check, ledger):
    if check['portfolio_id'] != ledger['portfolio_id']:
        raise ValueError('Ping and current portfolio do not match.')
    ids = check['new_bets']
    if not isinstance(ids, list) or len(ids) != len(set(ids)) or len(ids) > 3:
        raise ValueError('Invalid new_bets list.')
    bets = {bet['bet_id']: bet for bet in ledger['bets']}
    observations = check['bets']
    observed_ids = [row['bet_id'] for row in observations]
    if len(observed_ids) != len(set(observed_ids)) or not set(ids) <= set(observed_ids):
        raise ValueError('Invalid ping observations.')
    if not set(observed_ids) <= set(bets):
        raise ValueError('Ping contains unknown bets.')
    slots = [row for row in observations if row.get('status') not in ('won', 'lost', 'void')]
    if len(slots) > 3:
        raise ValueError('More than three occupied slots.')
    stamp = datetime.fromisoformat(check['checked_at'])
    if stamp.tzinfo is None:
        raise ValueError('Ping timestamp must include a timezone.')
    lines = [f'Spelstatus {stamp.astimezone(ZONE):%d/%m kl. %H.%M}', 'Pappersportfölj']
    if not ids:
        lines.append('Inga nya spel.')
    for index in range(3):
        if index >= len(slots):
            lines.append(f'Spel {index + 1}: Ledigt')
            continue
        observation = slots[index]
        bet = bets[observation['bet_id']]
        new = ' [NYTT]' if bet['bet_id'] in ids else ''
        start = datetime.fromisoformat(
            (observation.get('current_scheduled_start') or bet['scheduled_start']).replace('Z', '+00:00')
        )
        if start.tzinfo is None:
            raise ValueError('Match start must include a timezone.')
        state = observation.get('match_status')
        if observation.get('status') == 'review':
            status = 'Oklar avräkning'
        else:
            status = {
                'NOT_STARTED': 'Spel bokfört – inväntar matchstart',
                'STARTED': 'Pågående', 'P': 'Pågående', 'LIVE': 'Pågående',
                'POSTPONED': 'Uppskjuten', 'DELAYED': 'Försenad',
                'SUSPENDED': 'Tillfälligt avbruten', 'INTERRUPTED': 'Tillfälligt avbruten',
                'F': 'Slutresultat inväntar kontroll',
            }.get(state, 'Oklar status')
        score = observation.get('score')
        if isinstance(score, str) and score.strip():
            status += ' | ' + score
        odds = f"{Decimal(str(bet['odds'])):.2f}".replace('.', ',')
        ta_odds = f"{Decimal(str(bet['ta_odds'])):.2f}".replace('.', ',')
        diff = 100 * (1 / Decimal(str(bet['ta_odds'])) - 1 / Decimal(str(bet['odds'])))
        diff_text = f'{diff:+.1f}'.replace('.', ',')
        stake = f"{Decimal(str(bet['stake_sek'])):.2f}".replace('.', ',')
        lines.extend([
            f"Spel {index + 1}{new}: {bet['player_name']} mot {bet['opponent_name']}",
            status,
            f"{bet['tournament']}, {start.astimezone(ZONE):%d/%m %H.%M} (prel.) | {stake} kr",
            f'Svenska Spel (låst) {odds} | TA {ta_odds} | Diff {diff_text} pp',
        ])
    if 'realized_net_sek' in check and 'open_stake_sek' in check:
        net = f"{Decimal(str(check['realized_net_sek'])):.2f}".replace('.', ',')
        opened = f"{Decimal(str(check['open_stake_sek'])):.2f}".replace('.', ',')
        lines.append(f'Pappersnetto {net} kr | Öppen insats {opened} kr')
    message = '\n'.join(lines)
    if len(message) > 1024:
        raise ValueError('Notification exceeds Pushover message limit.')
    return message


def notify(check_path, preview=False, attachment=None):
    check_path = Path(check_path).resolve()
    tracking = PROJECT_ROOT.resolve() / 'tracking'
    if check_path.parent != (tracking / 'checks').resolve() or check_path.suffix != '.json':
        raise ValueError('Choose a current tracking/checks JSON file.')
    check = json.loads(check_path.read_text())
    ledger = json.loads((tracking / 'bets.json').read_text())
    message = message_for(check, ledger)
    if attachment is not None:
        attachment = Path(attachment).resolve()
        if not attachment.is_file():
            raise ValueError('The poster attachment does not exist.')
        message = 'Spelstatus'
    if preview:
        print(message)
        if attachment is not None:
            print(f'Attachment: {attachment}')
        return 0
    if not SENDER.is_file():
        raise ValueError('The shared Pushover skill is not installed.')

    folder = tracking / 'notifications'
    folder.mkdir(exist_ok=True)
    receipt = folder / check_path.name
    record = {
        'check_file': str(check_path.relative_to(PROJECT_ROOT.resolve())),
        'checked_at': check['checked_at'], 'portfolio_id': check['portfolio_id'],
        'new_bets': check['new_bets'], 'message': message, 'status': 'attempted',
        'attempted_at': datetime.now(ZONE).isoformat(),
    }
    if attachment is not None:
        record['attachment'] = str(attachment)
    # Claim this ping before sending: an interrupted/uncertain send is not retried.
    try:
        with receipt.open('x') as output:
            json.dump(record, output, ensure_ascii=False, indent=2)
            output.write('\n')
    except FileExistsError:
        previous = json.loads(receipt.read_text())
        print('This ping already has a notification attempt; nothing resent.')
        return 0 if previous.get('status') == 'accepted' else 1

    details = ''
    try:
        command = [sys.executable, str(SENDER), '--title', 'ATP-betting – ping']
        if attachment is not None:
            command.extend(['--attachment', str(attachment)])
        result = subprocess.run(
            command,
            input=message, text=True, capture_output=True, timeout=25,
        )
        accepted = result.returncode == 0
        if not accepted:
            details = result.stderr.strip()
    except (OSError, subprocess.TimeoutExpired):
        accepted = False
    record['status'] = 'accepted' if accepted else 'failed_or_unknown'
    record['finished_at'] = datetime.now(ZONE).isoformat()
    receipt.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    if accepted:
        print('Pushover accepted the ping notification.')
        return 0
    print('Pushover failed or its outcome is unknown. No automatic retry.', file=sys.stderr)
    if details:
        print(details, file=sys.stderr)
    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('check', type=Path, help='Completed ping JSON in tracking/checks')
    parser.add_argument('--preview', action='store_true', help='Print text without sending or logging')
    parser.add_argument('--attachment', type=Path, help='Current poster; replaces the text summary with Spelstatus')
    args = parser.parse_args()
    try:
        return notify(args.check, args.preview, args.attachment)
    except (OSError, ValueError, KeyError, TypeError):
        print('Unable to prepare notification; check the ping, ledger and Pushover skill.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
