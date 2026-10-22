# Tre spelkandidater

Kontrollerat 21 oktober 2026 kl. 19.57 Europe/Stockholm. Urval bland 16 kommande ATP-singelmatcher 21–23 oktober i Oddset-flödet. Alla tre matcher är markerade upcoming utan score vid slutkontrollen. Underlag Hard verifierat genom aktuella turneringsmetadata.

| Prioritet | Spel | Svensk start | Svenska Spel | TA | GPT | Modell-EV | Bedömd lägsta spelgräns |
|---|---|---|---|---|---|---|---|
| 1 | Francisco Cerundolo mot Clement Chidekh | 23/10 13.30 | 1.58 | 1.21 | 1.25 | 23.9% | 1.45 |
| 2 | Adrian Mannarino mot Nikoloz Basilashvili | 23/10 08.30 | 2.17 | 1.62 | 1.71 | 27.4% | 2.00 |
| 3 | Brandon Nakashima mot Kyrian Jacquet | 22/10 20.10 | 1.50 | 1.28 | 1.33 | 11.7% | 1.45 |

1. Stort prisutrymme mot modellerna och högre etablerad nivå. Dagens vinst mot Damm bekräftad i ATP-flödet; Chidekhs form är den främsta invändningen.
2. Modellerna gör honom till favorit trots outsiderpris. Dagens seger över Rublev bekräftad i ATP-flödet. Basilashvilis 8–2 i senaste tio registrerade matcher inklusive kval motiverar försiktighet.
3. Starkare hardcourt-Elo och 26–13 i registrerade hardcourt-matcher 2026. Jacquet är 7–3 senaste tio inklusive kval och har slagit Berrettini här.

Bortval: Machac: 4–6 last ten registered matches vs Khachanov 7–3; Mannarino chosen instead after current ATP result confirmation. Dzumhur: challenger-level winning run vs Bergs recent Shanghai round of 16 incl Alcaraz win. Altmaier: 5–13 on registered hardcourt matches in 2026 vs Gojo strong current qualifying form.

Begränsningar:
- Subjective shortlist after TA-EV screening, not a strict top-three model ranking.
- TA/GPT prices include existing 5% probability markup and are not independent confirmations.
- EV uses margin-free TA probability; it is conditional on model accuracy.
- Historical dates are event start dates; same-event order is inferred by round.
- Form includes qualifying, Challenger and Davis/Laver Cup matches, Completed/Aborted, excludes walkovers.
- Database history is behind current results; ATP live feed confirms Cerundolo vs Damm and Mannarino vs Rublev.
- No comprehensive verified injury assessment; Hard Elo does not distinguish indoor/outdoor.
- Minimum odds are subjective thresholds allowing for form/model uncertainty, not outputs of a validated calibration.

Källor:
- https://tennis.egelberg.se/api/oddset
- https://tennis.egelberg.se/api/events/current
- https://tennis.egelberg.se/api/matches/live
- Direct MariaDB PLAYER_ODDS, WIN_PROBABILITY_TA, players, matches, events

Spelgränserna är subjektiva och är satta högre än TA:s marginalfria nollpunkter (cirka 1,28, 1,70 och 1,34) för att ge utrymme för osäker form och modellfel. Ingen ny kalibrerad vinstchans påstås.

Rådata och metod: oddset.json, events-current.json, screening.json, recent-query.sql, recent-params.json, recent.py, recent.json, profiles.json, atp-live.json, final-odds-check.json och picks.json. Modellresultaten kommer från direkt MariaDB; ingen data/schemaändring gjord.
