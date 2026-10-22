WITH obs AS (
SELECT m.id,m.winner AS player_id,1 AS won,m.loser AS opponent_id,m.loser_rank AS opponent_rank,e.date,e.id AS event_id,e.name,e.type,e.surface,m.round,m.score,m.status
FROM matches m JOIN events e ON e.id=m.event WHERE m.winner IN (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) AND e.date BETWEEN '2025-10-22' AND '2026-10-22' AND m.status IN ('Completed','Aborted')
UNION ALL
SELECT m.id,m.loser AS player_id,0 AS won,m.winner AS opponent_id,m.winner_rank AS opponent_rank,e.date,e.id AS event_id,e.name,e.type,e.surface,m.round,m.score,m.status
FROM matches m JOIN events e ON e.id=m.event WHERE m.loser IN (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) AND e.date BETWEEN '2025-10-22' AND '2026-10-22' AND m.status IN ('Completed','Aborted')
) SELECT obs.*,p.name AS opponent FROM obs LEFT JOIN players p ON p.id=obs.opponent_id ORDER BY date DESC, CASE round WHEN 'F' THEN 10 WHEN 'SF' THEN 9 WHEN 'QF' THEN 8 WHEN 'R16' THEN 7 WHEN 'R32' THEN 6 WHEN 'R64' THEN 5 WHEN 'R128' THEN 4 WHEN 'Q3' THEN 3 WHEN 'Q2' THEN 2 WHEN 'Q1' THEN 1 ELSE 0 END DESC,id DESC