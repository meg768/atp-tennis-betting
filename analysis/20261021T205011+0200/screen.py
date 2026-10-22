from pathlib import Path
import sys,json
from datetime import datetime
from zoneinfo import ZoneInfo
sys.path.insert(0, str(Path.home() / ".agents/skills/atp-tennis/scripts"))
import database
p=Path(__file__).parent
raw=json.loads((p/'svenskaspel-raw.json').read_text())
items=raw['response']['events']
events=database.execute("SELECT id,name,date,type,surface FROM events WHERE id IN ('2026-9410','2026-7485','2026-496')")[0]['rows']
(p/'events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2,default=str))
eventmap={('Bryssel' if e['name']=='Brussels' else e['name']):e for e in events}
rows=[];names=set()
for item in items:
 e=item['event']
 if e['state']!='NOT_STARTED' or e['group'] not in eventmap:continue
 if datetime.fromisoformat(e['start'].replace('Z','+00:00'))<=datetime.now(ZoneInfo('Europe/Stockholm')):continue
 offer=next((o for o in item.get('betOffers',[]) if o.get('criterion',{}).get('englishLabel')=='Match Odds'),None)
 if not offer:continue
 for o in offer.get('outcomes',[]):names.add(o['participant'])
lookup={}
for name in sorted(names):
 ident=database.execute('SELECT PLAYER_LOOKUP(%s) AS id',(name,))[0]['rows'][0]['id']
 if ident:
  profile=database.execute('SELECT id,name,`rank`,age,elo_rank_hard FROM players WHERE id=%s',(ident,))[0]['rows']
  lookup[name]=profile[0] if profile else None
(p/'profiles.json').write_text(json.dumps(lookup,ensure_ascii=False,indent=2,default=str))
for item in items:
 e=item['event']
 if e['state']!='NOT_STARTED' or e['group'] not in eventmap:continue
 if datetime.fromisoformat(e['start'].replace('Z','+00:00'))<=datetime.now(ZoneInfo('Europe/Stockholm')):continue
 event=eventmap[e['group']]
 offer=next((o for o in item.get('betOffers',[]) if o.get('criterion',{}).get('englishLabel')=='Match Odds'),None)
 if not offer or len(offer.get('outcomes',[]))!=2:continue
 a,b=offer['outcomes']
 if any(o.get('status')!='OPEN' or not o.get('odds') or not lookup.get(o['participant']) for o in (a,b)):continue
 aid,bid=(lookup[o['participant']]['id'] for o in (a,b))
 probabilities=database.execute('SELECT WIN_PROBABILITY_TA(%s,%s,%s) AS p',(aid,bid,event['surface']))[0]['rows'][0]['p']
 if probabilities is None:continue
 pa=float(probabilities)
 for player,opp,prob in ((a,b,pa),(b,a,1-pa)):
  odds=player['odds']/1000
  ta=database.execute('SELECT ROUND(1 / LEAST(0.999, GREATEST(0.001, %s * 1.05)),2) AS odds',(prob,))[0]['rows'][0]['odds']
  row={'id':e['id'],'event_id':event['id'],'tournament':e['group'],'surface':event['surface'],'start':e['start'],'player':lookup[player['participant']],'opponent':lookup[opp['participant']],'ss':odds,'ta':ta,'p':prob,'ta_ev':prob*odds-1,'gap':odds/float(ta)-1,'outcome_id':player['id'],'offer_id':offer['id']}
  rows.append(row)
rows.sort(key=lambda r:r['ta_ev'],reverse=True)
(p/'screening.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
for r in rows[:15]:print(r['player']['name'],'vs',r['opponent']['name'],'SS',r['ss'],'TA',r['ta'],'TA-EV',round(100*r['ta_ev'],1),'start',r['start'],flush=True)
