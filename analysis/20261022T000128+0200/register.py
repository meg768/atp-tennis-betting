"""Register this manually reviewed selection once, with a fresh 24-hour check."""
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0, str(Path.home() / ".agents/skills/atp-tennis/scripts"))
import svenskaspel
from zoneinfo import ZoneInfo
import json, os, tempfile

p = Path(__file__).resolve().parent
root = p.parents[1]
track = root / 'tracking'
zone = ZoneInfo('Europe/Stockholm')
source = svenskaspel.SOURCE
rows = json.loads((p / 'screening.json').read_text())
choices = [
    {
        'player_id': 'M0FH', 'minimum': '2.85', 'probability_subjective': 0.37,
        'rationale': 'Macháč är outsider, men 3,10 kräver bara cirka 32,3 % vinstchans. Hardcourt-Elo 1755 mot Khachanovs 1810 talar för en mindre nivåskillnad än oddsen antyder. Macháč vann första omgången 6–2, 6–0 enligt arrangören. Jag bedömer hans chans till ungefär 37 %, försiktigare än TA:s cirka 42 %, och kräver minst 2,85 för att ha viss marginal till osäkerheten.',
        'risk': 'Khachanov är rättmätig favorit: 7–3 på de senaste tio registrerade matcherna mot Macháčs 4–6 före den färska Almatysegern. Khachanov slog Sakamoto 6–2, 6–4 och vann deras enda registrerade inbördes möte. Macháčs lätta öppningsmotstånd bevisar inte toppform. Ingen fullständig aktuell skadebild har verifierats.',
        'sources': ['https://almatyopen.ktf.kz/en/schedule', 'https://www.protennislive.com/posting/2026/9410/op.pdf'],
    },
    {
        'player_id': 'VA25', 'minimum': '1.58', 'probability_subjective': 0.66,
        'rationale': 'Vacherots hardcourt-Elo är 1831 mot Van Assches 1709. De registrerade Tokyo-segrarna över Fils och Tsitsipas visar att han kan prestera mot starkt motstånd. Jag bedömer cirka 66 % vinstchans, försiktigare än TA:s cirka 67 %, jämfört med prisets nollpunktskrav på cirka 61,7 %. Ett subjektivt rättvist odds runt 1,52 motiverar spel först från 1,58; erbjudna 1,62 ger en mindre men tillräcklig marginal.',
        'risk': 'Van Assche har 26–11 på registrerade hardcourt-matcher 2026 och vann Lyonöppningen i två set. Vacherot har förlorat två av sina tre senaste registrerade matcher och går in efter bye. Elo skiljer inte mellan hardcourt inne och ute. Spelet har begränsad marginal och bedömningen är subjektiv.',
        'sources': ['https://www.protennislive.com/posting/2026/496/mds.pdf', 'https://www.protennislive.com/posting/2026/496/op.pdf'],
    },
]
notes = '''# Ny serie – urval inom 24 timmar

Magnus bad den 22 oktober 2026 att rensa och starta om. Den tidigare serien har arkiverats, inklusive kontrollhistorik, och ingår inte i det nya saldot. Gamla affischer gäller den tidigare serien.

12 ännu ej påbörjade ATP-singelmatcher hade öppna matchvinnarmarknader och planerad start inom de närmaste 24 timmarna vid det första uttaget strax efter midnatt svensk tid. Matchernas kalenderdag och underlag stöds av officiella spelscheman. Nytt pris, öppen marknad, matchidentitet, status och 24-timmarsgräns kontrolleras igen vid registreringen.

TA är vägledning. Ingen GPT-oddsfunktion har anropats. TA-priserna har redan 5 % marginal. Egna sannolikheter och spelgränser är subjektiva bedömningar, inte en kalibrerad modell eller TA:s sannolikheter.

## Bortval

- Nakashima–Jacquet: Nakashima är fortsatt favorit. Men priset har fallit till 1,45, Jacquet har vunnit sju av sina tio senaste registrerade matcher inklusive kval och slog Berrettini i två set. Jag kräver nu minst 1,50 för att kompensera för osäkerheten. Matchen återförs inte från den gamla serien.
- Altmaier–Gojo: TA-gynnsamt pris på Altmaier räcker inte. Hans registrerade hardcourt-facit 2026 är 5–13 mot Gojos 32–11 inklusive kval och lägre turneringsnivåer. Gojo har dessutom tre vinster i Lyon. Ingen vald sida.
- Goffin–Michelsen: största modellgapet på Goffin, men 2–8 senaste tio registrerade och 0–6 på hardcourt 2026 före hans färska Brysselseger. Michelsen 27–13 på hardcourt och enkel öppningsseger. Den färska segern mot Bertola verifieras i officiell lottning men undanröjer inte osäkerheten.
- Dzumhur–Bergs: Dzumhurs Olbia-titel är främst Challenger-underlag; Bergs slog Alcaraz i Shanghai och har starkare aktuella ATP-meriter. Inget spel trots positiv TA-screening.
- Atmane–Bellucci: två nyliga avbrott i Atmanes registrerade historik, Bellucci 9–1 på senaste tio registrerade. Det måttliga TA-gapet räcker inte.
- Övriga matcher: underlaget gav ingen tydligare egen fördel än de två valda spelen. Fyll inte den tredje platsen för kvotens skull.

## Begränsningar och underlag

MariaDB lästes direkt via scripts/database.py. Databasen ligger efter på en del aktuella matcher. Exempelvis saknas Macháč–Nurlanuly i uttaget men arrangörens schema visar 6–2, 6–0. Senaste-tio- och årsstatistik inkluderar alla registrerade nivåer och kval samt Completed/Aborted, inte Walkover. Turneringens datum är inte matchdatum; omgångsordning används inom samma turnering. Rankningar i databasen och lottningarnas seedningslistor kan avse olika uttag. Ingen fullständig skadebild eller särskild inomhusmodell har verifierats.

ATP:s live-API gav en Cloudflare-sida vid detta uttag. Svaret är sparat som atp-live-error.html och har inte använts som matchdata. Officiella spelscheman och lottningar samt arrangörens resultatsida kompletterar databasen. Preliminära starttider från Svenska Spels leverantörsflöde används i loggen.

## Källor

- MariaDB: WIN_PROBABILITY_TA, players, matches, events.
- Svenska Spels direkta leverantörsflöde: svenskaspel-raw.json och final-odds-check.json.
- https://almatyopen.ktf.kz/en/schedule
- https://www.protennislive.com/posting/2026/9410/op.pdf
- https://www.protennislive.com/posting/2026/496/mds.pdf
- https://www.protennislive.com/posting/2026/496/op.pdf
- https://www.protennislive.com/posting/2026/7485/mds.pdf
- https://www.protennislive.com/posting/2026/7485/op.pdf

Reproducerbart underlag: screening.json, profiles.json, recent.json, recent-query.sql, recent-params.json, head-to-head.json. register.py får inte köras igen för att skapa dubbletter.
'''
for c in choices:
    row = next(r for r in rows if r['player']['id'] == c['player_id'])
    notes += f"\n## {row['player']['name']} mot {row['opponent']['name']}\n\n{c['rationale']}\n\nRisk: {c['risk']}\n"
(p / 'assessment.md').write_text(notes)
failed_live = p / 'atp-live-raw.json'
if failed_live.exists():
    failed_live.rename(p / 'atp-live-error.html')
ledger = json.loads((track / 'bets.json').read_text())
assert ledger['portfolio_id'] == 'atp-tennis-betting-20261022T000128+0200'
assert ledger['bets'] == [], 'Stop: existing bets must not be overwritten.'
assert not (track / 'settlements.jsonl').read_text().strip()
fresh = svenskaspel.fetch()['response']
now = datetime.now(zone)
(p / 'final-odds-check.json').write_text(json.dumps({'checked_at': now.isoformat(), 'source': source, 'response': fresh}, ensure_ascii=False, indent=2))
bets = []
for c in choices:
    r = next(r for r in rows if r['player']['id'] == c['player_id'])
    item = next(x for x in fresh['events'] if x['event']['id'] == r['id'])
    e = item['event']
    assert e['state'] == 'NOT_STARTED' and not item.get('liveData')
    start = datetime.fromisoformat(e['start'].replace('Z', '+00:00'))
    assert now < start <= now + timedelta(hours=24)
    offer = next(o for o in item['betOffers'] if o['id'] == r['offer_id'] and o.get('criterion', {}).get('englishLabel') == 'Match Odds')
    assert len(offer['outcomes']) == 2
    out = next(o for o in offer['outcomes'] if o['id'] == r['outcome_id'])
    assert out['participant'] == r['player']['name'] and out['status'] == 'OPEN'
    assert {o['participant'] for o in offer['outcomes']} == {r['player']['name'], r['opponent']['name']}
    odds = Decimal(out['odds']) / Decimal(1000)
    assert odds >= Decimal(c['minimum'])
    assert odds == Decimal(str(r['ss'])), 'Stop and review changed price before booking.'
    bets.append({
        'bet_id': now.strftime('%Y%m%dT%H%M%S%z') + '-' + str(e['id']) + '-' + c['player_id'],
        'recommendation_date': now.date().isoformat(), 'recommended_at': now.isoformat(), 'registered_at': now.isoformat(),
        'oddset_match_id': e['id'], 'offer_id': offer['id'], 'outcome_id': out['id'],
        'event_id': r['event_id'], 'tournament': e['group'], 'surface': r['surface'], 'scheduled_start': e['start'],
        'player_id': c['player_id'], 'player_name': r['player']['name'], 'opponent_id': r['opponent']['id'], 'opponent_name': r['opponent']['name'],
        'odds': str(odds.quantize(Decimal('.01'))), 'ta_odds': r['ta'], 'ta_probability': r['p'],
        'minimum_odds_subjective': c['minimum'], 'probability_subjective': c['probability_subjective'], 'stake_sek': '100.00',
        'selection_method': 'Självständig matchanalys med TA som vägledning; inga GPT-odds. Start inom 24 timmar.',
        'rationale': c['rationale'], 'risk': c['risk'], 'recommendation_source': str(p.relative_to(root) / 'assessment.md'),
        'odds_source': source, 'additional_sources': c['sources'], 'odds_checked_at': now.isoformat(), 'status_at_registration': 'NOT_STARTED',
    })
identities = [(b['event_id'], tuple(sorted([b['player_id'], b['opponent_id']]))) for b in bets]
assert len(identities) == len(set(identities)) and len(bets) <= 3
assert json.loads((track / 'bets.json').read_text()) == ledger, 'Stop: ledger changed during review.'
ledger['bets'] = bets
fd, temp = tempfile.mkstemp(dir=track, prefix='.bets-', suffix='.json')
try:
    with os.fdopen(fd, 'w') as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2); f.write('\n')
    os.replace(temp, track / 'bets.json')
finally:
    if os.path.exists(temp): os.unlink(temp)
lines = ['# Speluppföljning', '', f'Ny serie, bokförd {now:%Y-%m-%d kl. %H.%M} Europe/Stockholm. Två simulerade spel à 100 kr. Den tidigare serien är arkiverad och ingår inte i saldot. Tidigare affischer gäller den gamla serien.', '', 'Aktuella odds, öppna marknader, ej påbörjad status och start inom 24 timmar verifierades direkt vid bokföringen.', '', '| Spel | Svensk start¹ | Låst odds | TA² | Insats | Status | Matchresultat | Utbetalning | Netto |', '|---|---|---:|---:|---:|---|---|---:|---:|']
for b in sorted(bets, key=lambda b: b['scheduled_start']):
    start = datetime.fromisoformat(b['scheduled_start'].replace('Z', '+00:00')).astimezone(zone)
    lines.append(f"| {b['player_name']} mot {b['opponent_name']} | {start:%d/%m %H.%M} | {b['odds']} | {b['ta_odds']} | 100 kr | Spel bokfört – inväntar matchstart | — | — | — |")
lines += ['', 'Registrerade insatser: 200 kr. Öppen insats: 200 kr. Realiserat netto: 0 kr.', 'Avgjorda spel: 0. ROI och träffprocent: ej beräkningsbara.', 'En ledig plats. Inget tredje spel bedömdes tillräckligt bra till aktuellt pris.', '', '¹ Starttiderna är preliminära. ² TA inkluderar redan 5 % marginal.', '', '## Bedömning']
for b in bets:
    lines += ['', f"**{b['player_name']}**: {b['rationale']}", f"Risk: {b['risk']}"]
lines += ['', 'Fullständigt analysunderlag: ' + str(p.relative_to(root) / 'assessment.md') + '. Ingen schemaläggning.']
(track / 'overview.md').write_text('\n'.join(lines) + '\n')
check = {'checked_at': now.isoformat(), 'portfolio_id': ledger['portfolio_id'], 'action': 'initial_registration_after_reset', 'source': source, 'bets': [{'bet_id': b['bet_id'], 'match_status': 'NOT_STARTED', 'scheduled_start': b['scheduled_start'], 'odds': b['odds']} for b in bets], 'open_stake_sek': '200.00', 'realized_net_sek': '0.00'}
(track / 'checks' / (now.strftime('%Y%m%dT%H%M%S%z') + '.json')).write_text(json.dumps(check, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(check, ensure_ascii=False, indent=2))
