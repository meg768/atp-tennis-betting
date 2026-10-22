"""Register the reviewed new paper bet and report the full current series."""
from pathlib import Path
from datetime import datetime,timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo
import sys
sys.path.insert(0, str(Path.home() / ".agents/skills/atp-tennis/scripts"))
import svenskaspel
import json,os,tempfile
p=Path(__file__).resolve().parent;root=p.parents[1];t=root/'tracking';zone=ZoneInfo('Europe/Stockholm')
original=(t/'bets.json').read_bytes();ledger=json.loads(original);old_bets=json.loads(original)['bets'];latest={}
for line in (t/'settlements.jsonl').read_text().splitlines():
 if line.strip():e=json.loads(line);latest[e['bet_id']]=e
assert len([b for b in old_bets if latest.get(b['bet_id'],{}).get('status') not in ('won','lost','void')])==1
r=next(r for r in json.loads((p/'screening.json').read_text()) if r['player']['id']=='C0AU' and r['opponent']['id']=='C0BH')
key=(r['event_id'],tuple(sorted([r['player']['id'],r['opponent']['id']])))
assert key not in {(b['event_id'],tuple(sorted([b['player_id'],b['opponent_id']]))) for b in old_bets},'Duplicate: do not register.'
u=svenskaspel.SOURCE
raw=svenskaspel.fetch()['response']
now=datetime.now(zone)
(p/'final-odds-check.json').write_text(json.dumps({'checked_at':now.isoformat(),'source':u,'response':raw},ensure_ascii=False,indent=2)+'\n')
i=next(i for i in raw['events'] if i['event']['id']==r['id']);ev=i['event'];start=datetime.fromisoformat(ev['start'].replace('Z','+00:00'))
assert ev['state']=='NOT_STARTED' and not i.get('liveData') and now<start<=now+timedelta(hours=24)
offer=next(o for o in i['betOffers'] if o['id']==r['offer_id'] and o.get('criterion',{}).get('englishLabel')=='Match Odds')
assert {o['participant'] for o in offer['outcomes']}=={r['player']['name'],r['opponent']['name']}
out=next(o for o in offer['outcomes'] if o['id']==r['outcome_id']);assert out['status']=='OPEN'
odds=Decimal(out['odds'])/Decimal(1000);assert odds==Decimal(str(r['ss'])) and odds>=Decimal('1.50')
reason='Cerúndolos etablerade nivå och hardcourt-Elo 1840 mot Chidekhs 1616 samt segern över Damm 6–4, 7–6(4) talar för favoriten. 1,56 kräver cirka 64,1 % vinstchans; min subjektiva bedömning är ungefär 69 %, försiktigare än TA:s cirka 78,4 %. Rättvist odds omkring 1,45; lägsta spelgräns 1,50 ger viss marginal till osäkerheten.'
risk='Chidekh är 9–1 på de senaste tio registrerade matcherna och har fyra raka tvåsetsvinster i Bryssel inklusive kval, bland annat mot Van de Zandschulp och Fearnley. Hans aktuella nivå kan vara högre än långtidsmodellen. Ingen komplett aktuell skadebild eller separat inomhusmodell har verifierats; sannolikheten är en subjektiv bedömning.'
b={'bet_id':now.strftime('%Y%m%dT%H%M%S%z')+'-'+str(ev['id'])+'-C0AU','recommendation_date':now.date().isoformat(),'recommended_at':now.isoformat(),'registered_at':now.isoformat(),'oddset_match_id':ev['id'],'offer_id':offer['id'],'outcome_id':out['id'],'event_id':r['event_id'],'tournament':ev['group'],'surface':r['surface'],'scheduled_start':ev['start'],'player_id':'C0AU','player_name':r['player']['name'],'opponent_id':'C0BH','opponent_name':r['opponent']['name'],'odds':str(odds.quantize(Decimal('.01'))),'ta_odds':r['ta'],'ta_probability':r['p'],'minimum_odds_subjective':'1.50','probability_subjective':0.69,'stake_sek':'100.00','selection_method':'Självständig matchanalys med TA som vägledning; inga GPT-odds. Start inom 24 timmar.','rationale':reason,'risk':risk,'recommendation_source':str(p.relative_to(root)/'assessment.md'),'odds_source':u,'additional_sources':['https://www.protennislive.com/posting/2026/7485/mds.pdf','https://www.protennislive.com/posting/2026/7485/op.pdf'],'odds_checked_at':now.isoformat(),'status_at_registration':'NOT_STARTED'}
all_bets=old_bets+[b];observations=[]
for bet in all_bets:
 e=latest.get(bet['bet_id'],{})
 if e.get('status') in ('won','lost','void'):
  observations.append({'bet_id':bet['bet_id'],'match_status':e['match_status'],'status':e['status'],'score':e['score'],'winner_id':e['winner_id'],'source':e['source'],'source_match_id':e['source_match_id'],'current_scheduled_start':bet['scheduled_start']})
 else:
  item=next(i for i in raw['events'] if i['event']['id']==bet['oddset_match_id']);event=item['event']
  assert event['state']=='NOT_STARTED' and not item.get('liveData')
  assert {event['homeName'],event['awayName']}=={bet['player_name'],bet['opponent_name']}
  observations.append({'bet_id':bet['bet_id'],'match_status':'NOT_STARTED','status':'pending','score':None,'winner_id':None,'source':u,'source_match_id':bet['oddset_match_id'],'current_scheduled_start':event['start']})
assert (t/'bets.json').read_bytes()==original
ledger['bets']=all_bets
fd,tmp=tempfile.mkstemp(dir=t,prefix='.bets-',suffix='.json')
try:
 with os.fdopen(fd,'w') as f:json.dump(ledger,f,ensure_ascii=False,indent=2);f.write('\n')
 os.replace(tmp,t/'bets.json')
finally:
 if os.path.exists(tmp):os.unlink(tmp)
settled=[bet for bet in all_bets if latest.get(bet['bet_id'],{}).get('status') in ('won','lost','void')]
opened=[bet for bet in all_bets if bet not in settled]
net=sum((Decimal(latest[bet['bet_id']]['net_sek']) for bet in settled),Decimal('0'))
open_stake=sum((Decimal(bet['stake_sek']) for bet in opened),Decimal('0'))
actual_open=sum((Decimal(bet['user_reported_actual_bet']['stake_sek']) for bet in opened if bet.get('user_reported_actual_bet')),Decimal('0'))
actual_net=sum((Decimal(latest[bet['bet_id']]['actual_net_sek']) for bet in settled if bet.get('user_reported_actual_bet')),Decimal('0'))
roi_stakes=sum((Decimal(bet['stake_sek']) for bet in settled if latest[bet['bet_id']]['status'] in ('won','lost')),Decimal('0'))
roi=(net/roi_stakes*100).quantize(Decimal('.1')) if roi_stakes else None
wins=sum(latest[bet['bet_id']]['status']=='won' for bet in settled);losses=sum(latest[bet['bet_id']]['status']=='lost' for bet in settled)
check={'checked_at':now.isoformat(),'portfolio_id':ledger['portfolio_id'],'source':u,'result_source':'https://app.atptour.com/api/v2/gateway/livematches/website?scoringTournamentLevel=tour','database_checked':True,'bets':observations,'new_bets':[b['bet_id']],'new_settlements':[e['bet_id'] for e in json.loads((p/'new-settlements.json').read_text())],'selection_assessment':str(p.relative_to(root)/'assessment.md'),'open_stake_sek':str(open_stake.quantize(Decimal('.01'))),'realized_net_sek':str(net.quantize(Decimal('.01'))),'actual_open_stake_sek':str(actual_open.quantize(Decimal('.01'))),'actual_realized_net_sek':str(actual_net.quantize(Decimal('.01'))),'wins':wins,'losses':losses,'roi_percent':str(roi),'ta_diff_unit':'percentage_points','ta_diff_formula':'100 * (1 / ta_odds - 1 / locked_odds)'}
(t/'checks'/(now.strftime('%Y%m%dT%H%M%S%z')+'.json')).write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
lines=['# Speluppföljning','',f'Senaste kontroll: {now:%Y-%m-%d kl. %H.%M} Europe/Stockholm. Macháč och Vacherot förlorade normala färdigspelade matcher enligt direkt ATP-live-API. Avräkningarna är sparade. MariaDB saknar ännu dessa slutresultat.','', 'Mannarino ligger kvar som pappersspel. Cerúndolo har bokförts som ett nytt pappersspel efter egen analys, färskt pris och 24-timmarskontroll. En plats är ledig. Den gamla arkiverade serien ingår inte i saldot.','','| Spel på | Motståndare | Typ | Svensk start¹ | Låst odds | TA² | Diff³ | Insats | Status | Matchresultat⁴ | Utbetalning | Netto |','|---|---|---|---|---:|---:|---:|---:|---|---|---:|---:|']
for bet in all_bets:
 o=next(o for o in observations if o['bet_id']==bet['bet_id']);sdate=datetime.fromisoformat(o['current_scheduled_start'].replace('Z','+00:00')).astimezone(zone)
 actual=bool(bet.get('user_reported_actual_bet'));typ='Faktisk insats bekräftad' if actual else 'Pappersspel – faktisk insats ej bekräftad'
 state={'lost':'Förlorat','won':'Vunnet','void':'Återbetalt'}.get(o['status'],'Spel bokfört – inväntar matchstart');sett=latest.get(bet['bet_id'],{})
 diff=((1/Decimal(str(bet['ta_odds']))-1/Decimal(bet['odds']))*100).quantize(Decimal('.1'))
 payout=sett.get('payout_sek','—');bnet=sett.get('net_sek','—')
 lines.append(f"| {bet['player_name']} | {bet['opponent_name']} | {typ} | {sdate:%d/%m %H.%M} | {bet['odds']} | {bet['ta_odds']} | {diff:+} pp | 100 kr | {state} | {o['score'] or '—'} | {payout} | {bnet} |")
lines+=['',f'Pappersserien: totalt 400 kr registrerat; öppen insats {open_stake:.0f} kr; utbetalningar 0 kr; realiserat netto {net:.0f} kr. Vinster {wins}, förluster {losses}, ROI {roi} %, träffprocent 0 %.',f'Magnus bekräftade faktiska spel: totalt 200 kr satsat; öppen insats {actual_open:.0f} kr; utbetalningar 0 kr; realiserat netto {actual_net:.0f} kr. Två förluster, ROI −100 %. Dessa spel ingår även i pappersserien och summorna ska inte adderas.','', '¹ Preliminära svenska tider. Historiska datum/tider för avgjorda spel avser ursprungligen registrerad planerad start. ² TA inkluderar redan 5 % marginal. ³ Diff i implicerad sannolikhet: (1/TA − 1/spelodds) × 100, i procentenheter (pp), inte relativ oddsskillnad eller förväntad avkastning. ⁴ Setställning från vald spelares sida.','','## Bedömningar vid bokföring']
for bet in all_bets:lines+=['',f"**{bet['player_name']}**: {bet['rationale']}",f"Risk: {bet['risk']}"]
lines+=['','Fullständigt nytt analysunderlag: '+str(p.relative_to(root)/'assessment.md')+'. Ingen schemaläggning.']
(t/'overview.md').write_text('\n'.join(lines)+'\n')
verify=json.loads((t/'bets.json').read_text());assert verify['bets'][:len(old_bets)]==old_bets
assert len(opened)==2 and len(settled)==2 and len(all_bets)==4
assert net==actual_net==Decimal('-200') and actual_open==0 and open_stake==Decimal('200')
assert len({(bet['event_id'],tuple(sorted([bet['player_id'],bet['opponent_id']]))) for bet in all_bets})==len(all_bets)
print(json.dumps(check,ensure_ascii=False,indent=2));print('NEW_BET',b['player_name'],b['odds'],'TA',b['ta_odds'],b['scheduled_start'])
