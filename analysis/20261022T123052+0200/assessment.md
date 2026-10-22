# Ping 22 oktober 2026 – nytt urval inom 24 timmar

Direktkontroll från kl. 12.30 svensk tid. Macháč–Khachanov är pågående, först 2–6, 0–0 från Macháčs sida enligt Svenska Spels leverantörsflöde. Direkt ATP-live-API bekräftar båda ATP-ID, Almaty 2026, MS011, status P och samma setställning. Vacherot–Van Assche är ännu NOT_STARTED i leverantörsflödet och schemalagd 22 oktober kl. 14.00 enligt officiellt schema. Inget verifierat slutresultat för något befintligt spel i MariaDB.

Tretton kommande ATP-singelmatcher med öppna matchvinnarmarknader och planerad start inom 24 timmar screenades med nytt oddsuttag och färsk direkt MariaDB. TA-priserna inkluderar redan 5 % marginal. Inga GPT-odds anropades. Vacherot är redan bokförd och får inte registreras igen trots ändrat erbjudet odds.

## Nytt val: Adrian Mannarino mot Nikoloz Basilashvili

Almaty 2026, ATP-ID ME82/BG23, leverantörens match-ID 1029578799. Planerad start 23 oktober kl. 08.30 svensk tid, även bekräftad i officiellt fredagsprogram. Uppmärksamma att nya spel är pappersspel tills Magnus uttryckligen bekräftat en faktisk insats.

Mannarino 2,18 kräver cirka 45,9 % vinstchans för nollresultat över tid. TA-priset är 1,62 och underliggande marginalfri TA-sannolikhet cirka 58,7 %. Min egen bedömning är betydligt försiktigare: ungefär jämn match, cirka 50 % chans för Mannarino. Ett subjektivt rättvist odds runt 2,00 med marginal för osäkerheten ger lägsta spelgräns 2,10. 2,18 är tillräckligt för 100 kr i pappersserien.

Skäl: färsk MariaDB bekräftar Mannarinos seger över Rublev 6–4, 3–6, 6–3 i Almaty samt över Cobolli i Shanghai. Det är bättre aktuellt stöd mot etablerat ATP-motstånd än enbart ett historiskt modellgap. Mannarino har 7–3 på de senaste tio registrerade matcherna. Jag bedömer att marknadens tydliga favoritskap för Basilashvili är för stort, men gör inte Mannarino till en stark favorit.

Risk: Basilashvili är 8–2 på de senaste tio registrerade matcherna och har vunnit fyra raka matcher i Almaty, alla i två set, inklusive kval. Mannarino har behövt två tresetare och belastningen kan väga tungt. Den senaste registrerade inbördes matchen i Shanghai avbröts vid 6–3, 2–2 till Mannarino och är inget bevis för en fullständig spelmässig seger. Ingen komplett aktuell skadebild har verifierats. Egen 50-procentsbedömning är subjektiv och inte kalibrerad.

## Övriga kandidater

- Goffin 8,50: stort TA-gap, men färsk historik är 3–7 senaste tio och 1–6 på hardcourt 2026. Segern mot Bertola ändrar inte den stora osäkerheten mot Michelsen. Avstå.
- Dzumhur 4,10: nu 8–2 senaste tio inklusive Olbia-titeln på Challenger-nivå och segern mot Prizmic här. Bergs har starkare aktuella ATP-meriter, inklusive Shanghai-segern mot Alcaraz. Jag har mindre förtroende för en egen sannolikhet tillräckligt över nollpunkten än för Mannarino. Avstå.
- Nakashima 1,46 är fortsatt under min subjektiva gräns 1,50 mot Jacquet. Altmaier har sjunkit till 1,96 mot en Gojo i stark aktuell kvalform; ingen vald sida.
- Moutet–Paul: Moutet har två segrar i Lyon men Paul har 7–3 senaste tio och 25–13 på registrerade hardcourt-matcher 2026 mot Moutets 4–6 och 8–9. Varken Moutet 3,90 eller Paul 1,25 ger tillräckligt stöd för ett nytt spel.
- Tsitsipas–Duckworth: båda har färska segrar, men Tsitsipas är 8–2 senaste tio mot Duckworths 4–6. Jag ser ingen tydlig fördel till erbjudna 1,22 respektive 4,25.
- Övriga priser ger inte tillräckligt bedömt spelvärde för att prioriteras före Mannarino. Urvalet är inte en automatisk sortering efter TA-gap.

## Källor och begränsningar

Direkt MariaDB: players, events, matches, WIN_PROBABILITY_TA. Senaste-tio- och årsfacit omfattar registrerade nivåer och kval, Completed/Aborted, inte Walkover. Datum är turneringsstart; ordning inom turnering härleds ur omgång. Ingen fullständig skadebild eller särskild inomhusmodell. Databasen kan ligga efter aktuella matcher. Slutkontroll av priser och status samt fullständig dubblettkontroll görs vid bokföringen.

- Svenska Spels leverantörsflöde: svenskaspel-raw.json och final-odds-check.json.
- https://app.atptour.com/api/v2/gateway/livematches/website?scoringTournamentLevel=tour (atp-live-raw.json och atp-live.json).
- https://www.protennislive.com/posting/2026/9410/op.pdf (fredag 23 oktober, Mannarino–Basilashvili kl. 11.30 Almaty).
- https://www.protennislive.com/posting/2026/496/op.pdf (Vacherot–Van Assche torsdag 22 oktober).
- Reproducerbar screening och historik: screen.py, screening.json, profiles.json, recent.py, recent.json, recent-query.sql, recent-params.json och mannarino-h2h.json.

Den arkiverade serien från före nollställningen ingår inte i den nya serien. Det nya Mannarino-valet bygger på dagens analys, nytt pris och ett nu godkänt 24-timmarsfönster; ingen gammal post återförs automatiskt. Deduplicera mot hela den aktuella seriens bets.json.
