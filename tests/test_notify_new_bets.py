"""Exercise notification formatting and deduplication without sending pushes."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess

from scripts import notify_new_bets as notifications


class NotificationTests(unittest.TestCase):
    def setUp(self):
        self.check = {'portfolio_id': 'current', 'checked_at': '2026-10-22T22:27:00+02:00',
                      'new_bets': ['new'], 'bets': [
                          {'bet_id': 'old', 'status': 'lost', 'match_status': 'F'},
                          {'bet_id': 'new', 'status': 'pending', 'match_status': 'NOT_STARTED'},
                      ]}
        self.ledger = {'portfolio_id': 'current', 'bets': [
            {'bet_id': 'old', 'player_name': 'Old player'},
            {'bet_id': 'new', 'player_name': 'Luca Van Assche',
             'opponent_name': 'Lorenzo Musetti', 'tournament': 'Lyon',
             'scheduled_start': '2026-10-23T18:10:00Z', 'odds': '2.90', 'ta_odds': 2.37,
             'stake_sek': '100.00'},
        ]}

    def test_open_slots_and_locked_values_are_reported(self):
        message = notifications.message_for(self.check, self.ledger)
        self.assertIn('Luca Van Assche mot Lorenzo Musetti', message)
        self.assertIn('Pappersportfölj', message)
        self.assertIn('23/10 20.10', message)
        self.assertIn('100,00 kr', message)
        self.assertIn('Svenska Spel (låst) 2,90 | TA 2,37 | Diff +7,7 pp', message)
        self.assertIn('Spel 1 [NYTT]', message)
        self.assertIn('Spel bokfört – inväntar matchstart', message)
        self.assertIn('Spel 2: Ledigt', message)
        self.assertIn('Spel 3: Ledigt', message)
        self.assertNotIn('Old player', message)

    def test_no_new_bets_still_produces_ping_summary(self):
        self.check['new_bets'] = []
        message = notifications.message_for(self.check, self.ledger)
        self.assertIn('Inga nya spel', message)
        self.assertIn('Luca Van Assche mot Lorenzo Musetti', message)
        self.assertNotIn('[NYTT]', message)

    def test_live_unknown_and_review_status_are_not_inferred_from_time(self):
        row = self.check['bets'][1]
        for status, state, expected in (('pending', 'STARTED', 'Pågående'),
                                        ('pending', 'POSTPONED', 'Uppskjuten'),
                                        ('pending', None, 'Oklar status'),
                                        ('review', 'F', 'Oklar avräkning')):
            with self.subTest(state=state):
                row.update(status=status, match_status=state, score='6–4, 2–1')
                message = notifications.message_for(self.check, self.ledger)
                self.assertIn(expected + ' | 6–4, 2–1', message)

    def test_other_portfolio_or_duplicate_ids_rejected(self):
        for change in ({'portfolio_id': 'archive'}, {'new_bets': ['new', 'new']}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                notifications.message_for(dict(self.check, **change), self.ledger)

    def run_notification(self, root, preview=False, attachment=None):
        tracking = root/'tracking'
        (tracking/'checks').mkdir(parents=True, exist_ok=True)
        (tracking/'bets.json').write_text(json.dumps(self.ledger))
        check_path = tracking/'checks'/'ping.json'
        check_path.write_text(json.dumps(self.check))
        with patch.object(notifications, 'PROJECT_ROOT', root), \
                patch.object(notifications, 'SENDER', Path(__file__)), \
                contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return notifications.notify(check_path, preview, attachment)

    def test_poster_uses_minimal_caption_and_is_sent_only_once(self):
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(notifications.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as send:
            root = Path(folder)
            poster = root/'poster.png'
            poster.write_bytes(b'poster fixture')
            self.assertEqual(self.run_notification(root, attachment=poster), 0)
            self.assertEqual(self.run_notification(root, attachment=poster), 0)
            send.assert_called_once()
            self.assertEqual(send.call_args.kwargs['input'], 'Spelstatus')
            self.assertEqual(send.call_args.args[0][-2:], ['--attachment', str(poster.resolve())])
            receipt = json.loads((root/'tracking/notifications/ping.json').read_text())
            self.assertEqual(receipt['attachment'], str(poster.resolve()))
            self.assertEqual(receipt['message'], 'Spelstatus')

    def test_missing_poster_does_not_send_or_claim_ping(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(notifications.subprocess, 'run') as send:
            root = Path(folder)
            with self.assertRaises(ValueError):
                self.run_notification(root, attachment=root/'missing.png')
            send.assert_not_called()
            self.assertFalse((root/'tracking/notifications').exists())

    def test_poster_preview_does_not_send_or_create_receipt(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(notifications.subprocess, 'run') as send:
            root = Path(folder)
            poster = root/'poster.png'
            poster.touch()
            self.assertEqual(self.run_notification(root, preview=True, attachment=poster), 0)
            send.assert_not_called()
            self.assertFalse((root/'tracking/notifications').exists())

    def test_success_sent_once_per_ping(self):
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(notifications.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as send:
            root = Path(folder)
            self.assertEqual(self.run_notification(root), 0)
            self.assertEqual(self.run_notification(root), 0)
            send.assert_called_once()
            self.assertEqual(json.loads((root/'tracking/notifications/ping.json').read_text())['status'], 'accepted')
            self.assertIn('Svenska Spel (låst) 2,90 | TA 2,37', send.call_args.kwargs['input'])

    def test_uncertain_send_is_not_retried(self):
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(notifications.subprocess, 'run', side_effect=subprocess.TimeoutExpired('sender', 25)) as send:
            root = Path(folder)
            self.assertEqual(self.run_notification(root), 1)
            self.assertEqual(self.run_notification(root), 1)
            send.assert_called_once()
            self.assertEqual(json.loads((root/'tracking/notifications/ping.json').read_text())['status'], 'failed_or_unknown')

    def test_preview_never_sends_or_creates_receipt(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(notifications.subprocess, 'run') as send:
            root = Path(folder)
            self.assertEqual(self.run_notification(root, preview=True), 0)
            send.assert_not_called()
            self.assertFalse((root/'tracking/notifications').exists())


if __name__ == '__main__':
    unittest.main()
