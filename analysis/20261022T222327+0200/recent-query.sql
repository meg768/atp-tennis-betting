WITH observations AS (
 SELECT m.id,m.event,m.round,m.status,m.score,m.winner AS player_id,m.loser AS opponent_id,m.loser_rank AS opponent_rank,1 AS won,e.date AS event_date,e.name AS tournament,e.type,e.surface
 FROM matches m JOIN events e ON e.id=m.event
 WHERE m.winner IN (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) AND e.date BETWEEN %s AND %s AND m.status IN ('Completed','Aborted')
 UNION ALL
 SELECT m.id,m.event,m.round,m.status,m.score,m.loser AS player_id,m.winner AS opponent_id,m.winner_rank AS opponent_rank,0 AS won,e.date,e.name,e.type,e.surface
 FROM matches m JOIN events e ON e.id=m.event
 WHERE m.loser IN (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) AND e.date BETWEEN %s AND %s AND m.status IN ('Completed','Aborted')
) SELECT o.*,p.name AS opponent_name FROM observations o LEFT JOIN players p ON p.id=o.opponent_id
ORDER BY event_date DESC, CASE round WHEN 'F' THEN 10 WHEN 'SF' THEN 9 WHEN 'QF' THEN 8 WHEN 'R16' THEN 7 WHEN 'R32' THEN 6 WHEN 'R64' THEN 5 WHEN 'R128' THEN 4 WHEN 'Q3' THEN 3 WHEN 'Q2' THEN 2 WHEN 'Q1' THEN 1 ELSE 0 END DESC,id DESC
