"""Apply this reviewed ping once; preserve all prior locked bets."""
from pathlib import Path
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from decimal import Decimal
import json,sys,os,tempfile
sys.path.insert(0, str(Path.home() / ".agents/skills/atp-tennis/scripts"))
import database
import svenskaspel
p=Path(__file__).resolve().parent;root=p.parents[1];t=root/'tracking';zone=ZoneInfo('Europe/Stockholm')
original=(t/'bets.json').read_bytes();ledger=json.loads(original);prior_bets=json.loads(original)['bets']
latest={}
for line in (t/'settlements.jsonl').read_text().splitlines():
 if line.strip():e=json.loads(line);latest[e['bet_id']]=e
assert len([b for b in ledger['bets'] if latest.get(b['bet_id'],{}).get('status') not in ('won','lost','void')])<3
screen=json.loads((p/'screening.json').read_text());r=next(r for r in screen if r['player']['id']=='ME82' and r['opponent']['id']=='BG23')
key=(r['event_id'],tuple(sorted([r['player']['id'],r['opponent']['id']])))
assert key not in {(b['event_id'],tuple(sorted([b['player_id'],b['opponent_id']]))) for b in ledger['bets']},'Duplicate in full ledger.'
url=svenskaspel.SOURCE
fresh=svenskaspel.fetch()['response']
now=datetime.now(zone)
(p/'final-odds-check.json').write_text(json.dumps({'checked_at':now.isoformat(),'source':url,'response':fresh},ensure_ascii=False,indent=2)+'\n')
item=next(i for i in fresh['events'] if i['event']['id']==r['id']);ev=item['event']
assert ev['state']=='NOT_STARTED' and not item.get('liveData')
start=datetime.fromisoformat(ev['start'].replace('Z','+00:00'));assert now<start<=now+timedelta(hours=24)
offer=next(o for o in item['betOffers'] if o['id']==r['offer_id'] and o.get('criterion',{}).get('englishLabel')=='Match Odds')
assert {o['participant'] for o in offer['outcomes']}=={r['player']['name'],r['opponent']['name']}
out=next(o for o in offer['outcomes'] if o['id']==r['outcome_id']);assert out['status']=='OPEN'
odds=Decimal(out['odds'])/Decimal(1000);assert odds>=Decimal('2.10') and odds==Decimal(str(r['ss']))
reason='Mannarinos färska seger över Rublev 6–4, 3–6, 6–3 och segern över Cobolli i Shanghai ger stöd mot etablerat ATP-motstånd. Priset 2,18 kräver cirka 45,9 % vinstchans. Jag bedömer matchen ungefär jämn, cirka 50 %, försiktigare än TA:s cirka 58,7 %, och kräver minst 2,10 för viss marginal till osäkerheten.'
risk='Basilashvili är 8–2 på de senaste tio registrerade matcherna och har fyra raka tvåsetsvinster i Almaty inklusive kval. Mannarino har behövt två tresetare. Deras senaste inbördes match avbröts; den räknas inte som en fullständig spelmässig seger. Egen sannolikhet är subjektiv och ingen fullständig aktuell skadebild har verifierats.'
bet={'bet_id':now.strftime('%Y%m%dT%H%M%S%z')+'-'+str(ev['id'])+'-ME82','recommendation_date':now.date().isoformat(),'recommended_at':now.isoformat(),'registered_at':now.isoformat(),'oddset_match_id':ev['id'],'offer_id':offer['id'],'outcome_id':out['id'],'event_id':r['event_id'],'tournament':ev['group'],'surface':r['surface'],'scheduled_start':ev['start'],'player_id':'ME82','player_name':r['player']['name'],'opponent_id':'BG23','opponent_name':r['opponent']['name'],'odds':str(odds.quantize(Decimal('.01'))),'ta_odds':r['ta'],'ta_probability':r['p'],'minimum_odds_subjective':'2.10','probability_subjective':0.50,'stake_sek':'100.00','selection_method':'Självständig matchanalys med TA som vägledning; inga GPT-odds. Start inom 24 timmar.','rationale':reason,'risk':risk,'recommendation_source':str(p.relative_to(root)/'assessment.md'),'odds_source':url,'additional_sources':['https://www.protennislive.com/posting/2026/9410/op.pdf'],'odds_checked_at':now.isoformat(),'status_at_registration':'NOT_STARTED'}
all_bets=ledger['bets']+[bet];observations=[];pending_events=[]
for b in all_bets:
 db=database.execute('SELECT id,event,round,winner,loser,score,status FROM matches WHERE event=%s AND ((winner=%s AND loser=%s) OR (winner=%s AND loser=%s))',(b['event_id'],b['player_id'],b['opponent_id'],b['opponent_id'],b['player_id']))[0]['rows']
 assert not db,'New database result requires settlement review before proceeding.'
 current=next(i for i in fresh['events'] if i['event']['id']==b['oddset_match_id']);e=current['event']
 assert {e['homeName'],e['awayName']}=={b['player_name'],b['opponent_name']}
 assert e['state'] in ('NOT_STARTED','STARTED')
 score=None
 if e['state']=='STARTED':
  sets=current.get('liveData',{}).get('statistics',{}).get('sets',{})
  a,c=sets.get('home',[]),sets.get('away',[])
  if e['homeName']!=b['player_name']:a,c=c,a
  score=', '.join(f'{x}–{y}' for x,y in zip(a,c) if x>=0 and y>=0) or None
  prev=latest.get(b['bet_id'],{})
  if prev.get('match_status')!='STARTED' or prev.get('score')!=score:
   pending_events.append({'bet_id':b['bet_id'],'checked_at':now.isoformat(),'status':'pending','match_status':'STARTED','score':score,'winner_id':None,'source':url,'source_match_id':b['oddset_match_id'],'note':'Pågående match. Ingen avräkning, utbetalning eller ytterligare insats. Setställning ur direkt leverantörsflöde, från vald spelares sida.'})
 observations.append({'bet_id':b['bet_id'],'match_status':e['state'],'score':score,'score_perspective':b['player_name'],'current_scheduled_start':e['start'],'database_results':db,'locked_odds':b['odds'],'stake_sek':b['stake_sek']})
assert (t/'bets.json').read_bytes()==original
assert len(all_bets)==3
ledger['bets']=all_bets
fd,tmp=tempfile.mkstemp(dir=t,prefix='.bets-',suffix='.json')
try:
 with os.fdopen(fd,'w') as f:json.dump(ledger,f,ensure_ascii=False,indent=2);f.write('\n')
 os.replace(tmp,t/'bets.json')
finally:
 if os.path.exists(tmp):os.unlink(tmp)
with (t/'settlements.jsonl').open('a') as f:
 for event in pending_events:f.write(json.dumps(event,ensure_ascii=False)+'\n')
for event in pending_events:latest[event['bet_id']]=event
open_bets=[b for b in all_bets if latest.get(b['bet_id'],{}).get('status') not in ('won','lost','void')]
paper_stake=sum((Decimal(b['stake_sek']) for b in open_bets),Decimal('0'))
actual_stake=sum((Decimal(b['user_reported_actual_bet']['stake_sek']) for b in open_bets if b.get('user_reported_actual_bet')),Decimal('0'))
net=sum((Decimal(e['net_sek']) for e in latest.values() if e['status'] in ('won','lost','void')),Decimal('0'))
check={'checked_at':now.isoformat(),'portfolio_id':ledger['portfolio_id'],'source':url,'secondary_source':'https://app.atptour.com/api/v2/gateway/livematches/website?scoringTournamentLevel=tour','database_checked':True,'bets':observations,'new_bets':[bet['bet_id']],'new_settlements':[],'new_status_events':len(pending_events),'selection_assessment':str(p.relative_to(root)/'assessment.md'),'open_stake_sek':str(paper_stake.quantize(Decimal('.01'))),'realized_net_sek':str(net.quantize(Decimal('.01'))),'actual_open_stake_sek':str(actual_stake.quantize(Decimal('.01'))),'actual_realized_net_sek':'0.00'}
(t/'checks'/(now.strftime('%Y%m%dT%H%M%S%z')+'.json')).write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
lines=['# Speluppföljning','',f'Senaste kontroll: {now:%Y-%m-%d kl. %H.%M} Europe/Stockholm. Macháč–Khachanov pågår, Vacherot–Van Assche inväntar start. Inga verifierade slutresultat. Mannarino–Basilashvili fyller tredje platsen som nytt pappersspel; Magnus har ännu inte bekräftat någon faktisk insats på det spelet.','', 'Ny serie startad 22 oktober kl. 00.01. Den arkiverade serien ingår inte i saldot. Låsta odds och insatser behålls.','','| Spel | Typ | Svensk start¹ | Låst odds | TA² | Insats | Status | Matchresultat | Utbetalning | Netto |','|---|---|---|---:|---:|---:|---|---|---:|---:|']
for b in all_bets:
 o=next(o for o in observations if o['bet_id']==b['bet_id']);sdate=datetime.fromisoformat(o['current_scheduled_start'].replace('Z','+00:00')).astimezone(zone)
 label='Faktisk insats bekräftad' if b.get('user_reported_actual_bet') else 'Pappersspel – faktisk insats ej bekräftad'
 state='Pågående' if o['match_status']=='STARTED' else 'Spel bokfört – inväntar matchstart'
 lines.append(f"| {b['player_name']} mot {b['opponent_name']} | {label} | {sdate:%d/%m %H.%M} | {b['odds']} | {b['ta_odds']} | 100 kr | {state} | {o['score'] or '—'} | — | — |")
lines+=['',f'Pappersserien: {paper_stake:.0f} kr i öppna insatser, {net:.0f} kr realiserat netto. Tre öppna spel, inga avgjorda spel. ROI och träffprocent saknas.',f'Magnus bekräftade faktiska spel: {actual_stake:.0f} kr i öppen insats, 0 kr realiserat netto. Detta är samma Macháč- och Vacherot-spel och ska inte adderas till pappersseriens insatser.','', '¹ Preliminära svenska tider. Macháčs tidigare planerade start kl. 10.00 hade flyttats till kl. 11.45 enligt aktuellt flöde; ursprunglig tid i bets.json behålls. Setställning visas från vald spelares sida och kan ändras snabbt. ² TA-priser inkluderar redan 5 % marginal.','','## Bedömningar']
for b in all_bets:lines+=['',f"**{b['player_name']}**: {b['rationale']}",f"Risk: {b['risk']}"]
lines+=['','## Bekräftade faktiska spel','','| Spel | Bekräftat odds | Faktisk insats |','|---|---:|---:|']
for b in all_bets:
 a=b.get('user_reported_actual_bet')
 if a:lines.append(f"| {b['player_name']} mot {b['opponent_name']} | {a['odds']} | {a['stake_sek']} kr |")
lines+=['','Speloperatör har inte uttryckligen angetts. Inga faktiska spel har placerats av assistenten.','Analys och färskt råunderlag: '+str(p.relative_to(root))+'. Ingen schemaläggning.']
(t/'overview.md').write_text('\n'.join(lines)+'\n')
verify=json.loads((t/'bets.json').read_text());assert verify['bets'][:len(prior_bets)]==prior_bets
assert paper_stake==Decimal('300') and actual_stake==Decimal('200') and net==0
print(json.dumps(check,ensure_ascii=False,indent=2))
