from pathlib import Path
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo
import sys
sys.path.insert(0, str(Path.home() / ".agents/skills/atp-tennis/scripts"))
import svenskaspel
import json,os,tempfile
p=Path(__file__).resolve().parent;root=p.parents[1];track=root/'tracking'
url=svenskaspel.SOURCE
fresh=svenskaspel.fetch()['response']
now=datetime.now(ZoneInfo('Europe/Stockholm'))
(p/'final-odds-check.json').write_text(json.dumps({'fetched_at':now.isoformat(),'url':url,'response':fresh},ensure_ascii=False,indent=2))
rows=json.loads((p/'screening.json').read_text())
choices=[
 ('C0AU',Decimal('1.45'),'Cerúndolo har den starkare etablerade nivån och vann mot Damm 6–4, 7–6(4) i dag, verifierat direkt från ATP. Ett pris på 1,58 kräver cirka 63,3 % vinstchans. Jag bedömer honom som tydligare favorit än den gränsen, men klart försiktigare än TA-modellens 78,4 %.','Chidekh är i stark form: 8–2 på senaste tio registrerade matcher inklusive kval och slog Fearnley 7–6(4), 6–2 enligt den officiella lottningen. Motiverar en mindre övertygad bedömning än TA.'),
 ('ME82',Decimal('2.00'),'Mannarino är ett spelbart outsiderpris: 2,17 kräver cirka 46,1 % vinstchans. Jag bedömer matchen närmare jämn än marknadens pris antyder. Segern över Rublev 6–4, 3–6, 6–3 är verifierad direkt från ATP och han slog även Cobolli i Shanghai enligt databasen. TA-priset 1,62 ger ytterligare stöd, men är inte min egen exakta sannolikhet.','Basilashvili är 8–2 på senaste tio registrerade matcher inklusive kval och har flera segrar på plats. Mannarinos ålder och två registrerade tresetare i Almaty gör att jag kräver minst 2,00.'),
 ('N0AE',Decimal('1.45'),'Nakashimas högre hardcourt-Elo (1868 mot 1682) och 26–13 på registrerade hardcourt-matcher 2026 talar för honom. Han slog Medjedovic i tre set här; jag bedömer hans vinstchans tillräckligt hög för 1,50, men med mindre spelvärdesmarginal än TA indikerar.','Jacquet är 7–3 på senaste tio registrerade matcher inklusive kval, har redan slagit Berrettini här och får spela på hemmaplan. Därför inget starkt favoritspel till vilket pris som helst; bedömd lägsta gräns 1,45.')]
ledger=json.loads((track/'bets.json').read_text())
assert not ledger['bets'],'Ledger no longer empty: do not overwrite existing bets.'
assert not (track/'settlements.jsonl').read_text().strip(),'Unexpected settlements: stop.'
bets=[]
for player_id,minimum,reason,risk in choices:
 old=next(x for x in rows if x['player']['id']==player_id)
 item=next(x for x in fresh['events'] if x['event']['id']==old['id'])
 e=item['event'];assert e['state']=='NOT_STARTED';assert not item.get('liveData')
 assert datetime.fromisoformat(e['start'].replace('Z','+00:00'))>now
 offer=next(o for o in item['betOffers'] if o.get('criterion',{}).get('englishLabel')=='Match Odds')
 outcome=next(o for o in offer['outcomes'] if o['id']==old['outcome_id'])
 assert outcome['status']=='OPEN'
 price=Decimal(outcome['odds'])/Decimal('1000');assert price>=minimum
 b={'bet_id':now.strftime('%Y%m%dT%H%M%S%z')+'-'+str(e['id'])+'-'+player_id,'recommendation_date':now.date().isoformat(),'recommended_at':now.isoformat(),'registered_at':now.isoformat(),'oddset_match_id':e['id'],'offer_id':offer['id'],'outcome_id':outcome['id'],'event_id':old['event_id'],'tournament':e['group'],'surface':old['surface'],'scheduled_start':e['start'],'player_id':player_id,'player_name':old['player']['name'],'opponent_id':old['opponent']['id'],'opponent_name':old['opponent']['name'],'odds':str(price.quantize(Decimal('.01'))),'ta_odds':old['ta'],'ta_probability':old['p'],'minimum_odds_subjective':str(minimum),'stake_sek':'100.00','selection_method':'Selfständing matchanalys med TA som vägledning; inga GPT-odds.','rationale':reason,'risk':risk,'recommendation_source':str(p.relative_to(root))+'/assessment.md','odds_source':url,'odds_checked_at':now.isoformat(),'status_at_registration':'NOT_STARTED'}
 bets.append(b)
assert len({b['oddset_match_id'] for b in bets})==3
ledger['bets']=bets
fd,tmp=tempfile.mkstemp(dir=track,prefix='.bets-',suffix='.json')
try:
 with os.fdopen(fd,'w') as f:json.dump(ledger,f,ensure_ascii=False,indent=2);f.write('\n')
 os.replace(tmp,track/'bets.json')
finally:
 if os.path.exists(tmp):os.unlink(tmp)
lines=['# Speluppföljning','',f"Registrerat {now.strftime('%Y-%m-%d kl. %H.%M')} Europe/Stockholm. Tre nya simulerade spel à 100 kr efter nollställningen. Odds och kommande status nyverifierade direkt i Svenska Spels leverantörsflöde.",'','| Spel | Svensk start¹ | Låst odds | TA² | Insats | Status | Matchresultat | Utbetalning | Netto |','|---|---|---:|---:|---:|---|---|---:|---:|']
for b in sorted(bets,key=lambda b:b['scheduled_start']):
 start=datetime.fromisoformat(b['scheduled_start'].replace('Z','+00:00')).astimezone(ZoneInfo('Europe/Stockholm')).strftime('%d/%m %H.%M')
 lines.append(f"| {b['player_name']} mot {b['opponent_name']} | {start} | {b['odds']} | {b['ta_odds']} | 100 kr | Kommande | — | — | — |")
lines+=['','Registrerade insatser: 300 kr. Öppen insats: 300 kr. Realiserat netto: 0 kr.','Avgjorda spel: 0. ROI och träffprocent: ej beräkningsbara.','Alla tre platser upptagna. ”Kommande” betyder redan bokfört pappersspel.','','¹ Starttiderna från Svenska Spels aktuella flöde är preliminära. ² TA inkluderar redan 5 % marginal.','','## Bedömning']
for b in bets:lines+=['',f"**{b['player_name']}**: {b['rationale']}",f"Risk: {b['risk']}"]
lines+=['','Källor: direkt MariaDB (WIN_PROBABILITY_TA, players, matches, events); Svenska Spels leverantörsflöde hos eu1.offering-api.kambicdn.com; ATP:s livematch-API; officiella lottningar för Bryssel och Lyon hos protennislive.com.','Analysunderlag: '+str(p.relative_to(root))+'. Ingen schemaläggning.']
(track/'overview.md').write_text('\n'.join(lines)+'\n')
notes=['# Nytt urval efter nollställning','',f'Uttag och låsning {now.isoformat()}. 15 kommande ATP-singelmatcher screenades från direkt Svenska Spel/Kambi-flöde; pågående Onclin–Struff uteslöts. Ingen GPT-rutin har anropats.','Urvalet är en självständig bedömning med TA som vägledning; TA-modell-EV användes för screening men styrde inte den slutliga rangordningen.','']
for b in bets:notes += [f"## {b['player_name']} mot {b['opponent_name']}",f"SS {b['odds']}, TA {b['ta_odds']}, insats 100 kr. Subjektiv spelgräns {b['minimum_odds_subjective']}.",b['rationale'],b['risk'],'']
notes += ['## Bortval','Machac: störst TA-EV men 4–6 senaste tio registrerade mot Khachanovs 7–3 och starkare etablerade motstånd. Dzumhur: Olbia-titel på Challenger-nivå jämförs med Bergs senaste Shanghai-åttondel inklusive seger över Alcaraz; större osäkerhet än vald trio. Altmaier: 5–13 på hardcourt under 2026 i databasen mot Gojos aktuella kvalform. Atmane: två nyliga avbrott och Bellucci 9–1 på senaste tio, svagt stöd för ett litet TA-gap. Vacherot: spelbar reserv, men Van Assches 26–11 på hardcourt i registrerad 2026-historik gör att jag inte prioriterar detta före vald trio.','', '## Begränsningar','Databasen ligger efter dagens matcher. ATP-flödet kompletterar dagens Cerúndolo–Damm och Mannarino–Rublev; Bryssels officiella lottning bekräftar Chidekh–Fearnley. Senaste-tio-statistik inkluderar kval och alla registrerade nivåer, Completed/Aborted, exklusive Walkover. Historikdatum avser turneringsstart; ordning inom turnering härleds från omgång. Hard-Elo skiljer inte inne/ute. Ingen fullständig skadebild har verifierats. Spelgränserna och den egna bedömningen är subjektiva; inga nya kalibrerade sannolikheter påstås.','', '## Direkta källor',url,'https://app.atptour.com/api/v2/gateway/livematches/website?scoringTournamentLevel=tour','https://www.protennislive.com/posting/2026/7485/mds.pdf','https://www.protennislive.com/posting/2026/496/mds.pdf','MariaDB via atp-tennis-skillens scripts/database.py','', 'Raw: svenskaspel-raw.json, final-odds-check.json, atp-live-raw.json, atp-live.json, screening.json, profiles.json, recent.json, recent-query.sql, recent-params.json. Reproducerbara skript: screen.py, recent.py, register.py. Kör inte register.py igen för att skapa dubbla spel.']
(p/'assessment.md').write_text('\n'.join(notes)+'\n')
print('Registered at:',now.isoformat())
for b in bets:print(b['player_name'],'vs',b['opponent_name'],b['odds'],'TA',b['ta_odds'],b['scheduled_start'])
