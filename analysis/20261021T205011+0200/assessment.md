# Nytt urval efter nollställning

Uttag och låsning 2026-10-21T20:52:58.306747+02:00. 15 kommande ATP-singelmatcher screenades från direkt Svenska Spel/Kambi-flöde; pågående Onclin–Struff uteslöts. Ingen GPT-rutin har anropats.
Urvalet är en självständig bedömning med TA som vägledning; TA-modell-EV användes för screening men styrde inte den slutliga rangordningen.

## Francisco Cerundolo mot Clement Chidekh
SS 1.58, TA 1.21, insats 100 kr. Subjektiv spelgräns 1.45.
Cerúndolo har den starkare etablerade nivån och vann mot Damm 6–4, 7–6(4) i dag, verifierat direkt från ATP. Ett pris på 1,58 kräver cirka 63,3 % vinstchans. Jag bedömer honom som tydligare favorit än den gränsen, men klart försiktigare än TA-modellens 78,4 %.
Chidekh är i stark form: 8–2 på senaste tio registrerade matcher inklusive kval och slog Fearnley 7–6(4), 6–2 enligt den officiella lottningen. Motiverar en mindre övertygad bedömning än TA.

## Adrian Mannarino mot Nikoloz Basilashvili
SS 2.17, TA 1.62, insats 100 kr. Subjektiv spelgräns 2.00.
Mannarino är ett spelbart outsiderpris: 2,17 kräver cirka 46,1 % vinstchans. Jag bedömer matchen närmare jämn än marknadens pris antyder. Segern över Rublev 6–4, 3–6, 6–3 är verifierad direkt från ATP och han slog även Cobolli i Shanghai enligt databasen. TA-priset 1,62 ger ytterligare stöd, men är inte min egen exakta sannolikhet.
Basilashvili är 8–2 på senaste tio registrerade matcher inklusive kval och har flera segrar på plats. Mannarinos ålder och två registrerade tresetare i Almaty gör att jag kräver minst 2,00.

## Brandon Nakashima mot Kyrian Jacquet
SS 1.50, TA 1.28, insats 100 kr. Subjektiv spelgräns 1.45.
Nakashimas högre hardcourt-Elo (1868 mot 1682) och 26–13 på registrerade hardcourt-matcher 2026 talar för honom. Han slog Medjedovic i tre set här; jag bedömer hans vinstchans tillräckligt hög för 1,50, men med mindre spelvärdesmarginal än TA indikerar.
Jacquet är 7–3 på senaste tio registrerade matcher inklusive kval, har redan slagit Berrettini här och får spela på hemmaplan. Därför inget starkt favoritspel till vilket pris som helst; bedömd lägsta gräns 1,45.

## Bortval
Machac: störst TA-EV men 4–6 senaste tio registrerade mot Khachanovs 7–3 och starkare etablerade motstånd. Dzumhur: Olbia-titel på Challenger-nivå jämförs med Bergs senaste Shanghai-åttondel inklusive seger över Alcaraz; större osäkerhet än vald trio. Altmaier: 5–13 på hardcourt under 2026 i databasen mot Gojos aktuella kvalform. Atmane: två nyliga avbrott och Bellucci 9–1 på senaste tio, svagt stöd för ett litet TA-gap. Vacherot: spelbar reserv, men Van Assches 26–11 på hardcourt i registrerad 2026-historik gör att jag inte prioriterar detta före vald trio.

## Begränsningar
Databasen ligger efter dagens matcher. ATP-flödet kompletterar dagens Cerúndolo–Damm och Mannarino–Rublev; Bryssels officiella lottning bekräftar Chidekh–Fearnley. Senaste-tio-statistik inkluderar kval och alla registrerade nivåer, Completed/Aborted, exklusive Walkover. Historikdatum avser turneringsstart; ordning inom turnering härleds från omgång. Hard-Elo skiljer inte inne/ute. Ingen fullständig skadebild har verifierats. Spelgränserna och den egna bedömningen är subjektiva; inga nya kalibrerade sannolikheter påstås.

## Direkta källor
https://eu1.offering-api.kambicdn.com/offering/v2018/svenskaspel/listView/tennis/atp/all/all/matches.json?channel_id=1&client_id=200&lang=sv_SE&market=SE&useCombined=true&useCombinedLive=true
https://app.atptour.com/api/v2/gateway/livematches/website?scoringTournamentLevel=tour
https://www.protennislive.com/posting/2026/7485/mds.pdf
https://www.protennislive.com/posting/2026/496/mds.pdf
MariaDB via scripts/database.py

Raw: svenskaspel-raw.json, final-odds-check.json, atp-live-raw.json, atp-live.json, screening.json, profiles.json, recent.json, recent-query.sql, recent-params.json. Reproducerbara skript: screen.py, recent.py, register.py. Kör inte register.py igen för att skapa dubbla spel.
