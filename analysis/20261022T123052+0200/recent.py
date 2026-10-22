from pathlib import Path
import sys,json
sys.path.insert(0, str(Path.home() / ".agents/skills/atp-tennis/scripts"))
import database
p=Path(__file__).parent
ids=sorted({x['player']['id'] for x in json.loads((p/'screening.json').read_text())})
marks=','.join(['%s']*len(ids))
sql=f'''WITH obs AS (
SELECT m.id,m.winner AS player_id,1 AS won,m.loser AS opponent_id,m.loser_rank AS opponent_rank,e.date,e.id AS event_id,e.name,e.type,e.surface,m.round,m.score,m.status
FROM matches m JOIN events e ON e.id=m.event WHERE m.winner IN ({marks}) AND e.date BETWEEN '2025-10-22' AND '2026-10-22' AND m.status IN ('Completed','Aborted')
UNION ALL
SELECT m.id,m.loser AS player_id,0 AS won,m.winner AS opponent_id,m.winner_rank AS opponent_rank,e.date,e.id AS event_id,e.name,e.type,e.surface,m.round,m.score,m.status
FROM matches m JOIN events e ON e.id=m.event WHERE m.loser IN ({marks}) AND e.date BETWEEN '2025-10-22' AND '2026-10-22' AND m.status IN ('Completed','Aborted')
) SELECT obs.*,p.name AS opponent FROM obs LEFT JOIN players p ON p.id=obs.opponent_id ORDER BY date DESC, CASE round WHEN 'F' THEN 10 WHEN 'SF' THEN 9 WHEN 'QF' THEN 8 WHEN 'R16' THEN 7 WHEN 'R32' THEN 6 WHEN 'R64' THEN 5 WHEN 'R128' THEN 4 WHEN 'Q3' THEN 3 WHEN 'Q2' THEN 2 WHEN 'Q1' THEN 1 ELSE 0 END DESC,id DESC'''
(p/'recent-query.sql').write_text(sql);(p/'recent-params.json').write_text(json.dumps(ids*2))
rows=database.execute(sql,tuple(ids*2))[0]['rows']
(p/'recent.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
for ident in ids:
 rs=[r for r in rows if r['player_id']==ident];hard=[r for r in rs if r['surface']=='Hard' and str(r['date'])>='2026-01-01']
 print(ident,'last10',sum(r['won'] for r in rs[:10]),'-',len(rs[:10])-sum(r['won'] for r in rs[:10]),'Hard2026',sum(r['won'] for r in hard),'-',len(hard)-sum(r['won'] for r in hard),flush=True)
 for r in rs[:5]:print(r['date'],r['name'],r['round'],'W' if r['won'] else 'L',r['opponent'],r['score'],r['status'],flush=True)
