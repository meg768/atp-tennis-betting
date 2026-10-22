# Projektkontext

Uppdaterad på Magnus begäran den 22 oktober 2026.

## Arbetsinstruktioner

- Läs och följ denna fil vid början av varje uppgift. Projektets instruktioner
  och sparade kontext är samlade här. Global `AGENTS.md` anger att denna fil
  ska läsas; projektet har ingen egen `AGENTS.md`.
- Ändra filen bara när Magnus uttryckligen ber att spara kontext eller
  uppdatera dokumentet. Respektera tidigare dokumenterade beslut.
- Läs `README.md` för urvalsmetoden och `tracking/README.md` för bokföringen.
- Placera inga faktiska spel. Magnus genomför själv sina faktiska insatser;
  assistenten analyserar, bokför och följer upp.
- Ingen commit eller push utan Magnus uttryckliga tillåtelse.

## Syfte och samarbete

- `atp-tennis-betting` är ett separat projekt för bettingdelen från
  `atp-tennis-chat`. Kommunicera kort och tydligt på svenska.
- Magnus vill undersöka om spel med TA-odds som vägledning är fördelaktiga
  över tid. Slutlig överenskommelse: gör en självständig analys av spelarnas
  vinstchanser, form, motstånd, underlag och osäkerheter. TA är vägledning;
  välj inte mekaniskt de största oddsgapen. Databasens GPT-odds ska hoppas över.
- Resultatet av denna serie mäter den samlade urvalsmetoden, inte TA isolerat.
- Grundserien är en pappersportfölj med 100 kr per rekommenderad match.
  Magnus har därefter själv placerat och bekräftat två faktiska spel;
  se nedan. Assistenten har inte placerat spelen. Nya rekommendationer
  är fortfarande pappersspel tills Magnus bekräftar en faktisk insats.

## Tre spelplatser och kommandot ”ping”

- Ha högst tre samtidigt öppna spel. Vid varje ping: kontrollera samtliga
  öppna matcher, avräkna verifierade slutresultat och fyll lediga platser
  med nya kommande matcher efter egen analys.
- Nya spel måste ha verifierad planerad matchstart efter bokföringstillfället
  och senast 24 timmar därefter. Det är ett rullande fönster, inte ett
  kalenderdygn. Kontrollera gränsen och ej påbörjad status vid bokföringen.
  Saknas bra kandidater eller verifierbar starttid ska platser stå tomma.
  Redan bokförda spel behålls även om starten flyttas utanför fönstret.
- Bokför nya spel före matchstart med då verifierade odds, insats, båda
  ATP-ID, turneringsupplaga, tid, analys och källor. Behåll ursprungliga
  odds och insatser. Byt inte ut öppna spel för att andra kandidater ser bättre ut.
- Ett nytt ping efter fem minuter ger normalt bara aktuell status. Skapa
  inga dubbla spel eller avräkningar. Om källor eller spelvärde inte räcker,
  låt platser stå tomma och ange varför.
- Kontrollera nya kandidater mot hela den aktuella seriens spellogg,
  inklusive alla datum och avgjorda spel. Samma turneringsupplaga och samma
  två ATP-ID i sorterad ordning identifierar matchen. Ändrat datum, odds,
  namnordning, vald sida eller leverantörs-ID gör den inte till ett nytt spel.
- Skriv status **”Spel bokfört – inväntar matchstart”**, med låst odds och
  insats bredvid. Magnus vill att det tydligt framgår att spelet redan är
  registrerat. ”Kommande” betyder redan bokfört spel och insatsen är öppen
  från registreringen. När matchen börjar ändras status till pågående; det medför
  ingen ytterligare insats. Uppskjutna eller oklara matcher behåller sin plats.
- Ett sent ping fungerar också: hämta slutresultaten i efterhand och avräkna
  de redan bokförda spelen. Skapa aldrig nya historiska spel retroaktivt.
- Ingen schemaläggning. Automationen ”Dagliga ATP-tips och spelresultat”
  med körning kl. 07.00 togs bort på Magnus begäran. Skapa ingen ersättare
  utan ny uttrycklig instruktion. Datorn behöver inte vara på mellan ping.

## Datakällor och odds

- Använd **inte `tennis.egelberg.se` överhuvudtaget**: inga anrop, ingen
  reservväg eller proxy, ingen drift eller schemaläggning där. Äldre
  analysfiler får behålla korrekt historisk källangivelse, men gamla
  snapshots från tjänsten får inte användas som nytt analysunderlag.
- MariaDB nås direkt via `scripts/database.py`, lokal Git-ignorerad `.env`
  och `.venv/bin/python`. Visa aldrig hemligheter. Endast läsning är
  auktoriserad; hjälpskriptet spärrar inte skrivande SQL tekniskt.
- Svenska Spels direkta leverantörsflöde är verifierat fungerande:
  `https://eu1.offering-api.kambicdn.com/offering/v2018/svenskaspel/listView/tennis/atp/all/all/matches.json`
  med `channel_id=1`, `client_id=200`, `lang=sv_SE`, `market=SE`,
  `useCombined=true`, `useCombinedLive=true`.
  Använd matchvinnarmarknaden `Match Odds`/`Matchodds`, kontrollera öppna
  utfall och dividera råoddsen med 1000. `NOT_STARTED` anger kommande,
  `STARTED` pågående. En försvunnen match är inte bevis för slutresultat.
- Kontrollera matchstatus och pris igen före ny bokföring. Visa starttider
  i `Europe/Stockholm`; tiderna kan vara preliminära.
- TA-oddsen har **redan 5 % marginal** och jämförs direkt med Svenska Spels
  odds. Lägg inte till en andra marginal och anpassa inte till Svenska Spels
  exakta överrundning.
- `WIN_PROBABILITY_TA(A,B,surface)` ger marginalfri sannolikhet `p`.
  TA-priset enligt databasens prissättning är
  `ROUND(1 / LEAST(0.999, GREATEST(0.001, p * 1.05)), 2)`; andra sidan använder
  `1-p`. Undvik `PLAYER_ODDS`, som också beräknar GPT-odds.
- Ett odds-prisgap är inte förväntad avkastning. Om modell-EV redovisas,
  använd marginalfri sannolikhet i `p * spelodds - 1` och märk det som
  villkorat modellresultat, inte automatiskt egen bedömning.
- Komplettera direkt från ATP, arrangören eller Tennis Abstract.
  Kontrollera åtkomsten till externa källor; anta inte att en direktintegration
  redan fungerar.
  Databashistoriken kan ligga efter dagens resultat. `events.date` är
  turneringsstart, inte matchdag. Var tydlig om statistik inkluderar kval
  och Challenger, och tolka inte bristfällig historik som fullständig.
- Direkt ATP-livematchkälla:
  `https://app.atptour.com/api/v2/gateway/livematches/website?scoringTournamentLevel=tour`.
  Vanlig urllib gav 403; curl med `--http1.1 --no-alpn`, webbläsar-User-Agent
  och Origin/Referer `https://app.atptour.com` har fungerat, men uttaget
  den 22 oktober gav en Cloudflare-sida. Använd inte HTML-felsvaret som
  matchdata. Spara rådata och
  kontrollera båda ATP-ID, turnering och status. Officiella lottningar finns
  även hos `www.protennislive.com/posting/ÅR/TURNERINGSID/mds.pdf`;
  åtkomsten varierar.

## Spellogg och resultat

- `tracking/bets.json` är källan för alla låsta spel.
- Valfritt `user_reported_actual_bet` på respektive spel sparar Magnus
  uttryckligen bekräftade faktiska insats och odds. Ändra inte pappersspelets
  ursprungliga odds eller tider. En bekräftelse skapar varken en ny matchpost
  eller ytterligare insats. Håll faktisk uppföljning skild från pappersserien
  så att samma 200 kr inte summeras till 400 kr. Använd de bekräftade faktiska
  oddsen för verkligt resultat. Speloperatör har ännu inte uttryckligen angetts;
  specialfall kräver därför kontroll av tillämpliga regler.
- `tracking/settlements.jsonl` innehåller avräkningshändelser, en per rad.
  Lägg till korrigeringar i stället för att skriva om historik; senaste
  händelsen per spel gäller. Undvik dubbletter vid oförändrat läge.
- `tracking/overview.md` visar alla bokförda matcher, även avslutade:
  vald spelare, motståndare, odds, insats, slutresultat, vinst/förlust,
  utbetalning och netto i kronor. Behåll historiken när platser fylls på.
- `tracking/checks/` sparar tidsstämplade kontroller och rådata.
  `tracking/README.md` innehåller den fullständiga arbetsgången.
- Använd `Decimal`. Normal vinst: utbetalning = insats × låst odds,
  netto = utbetalning − insats. Normal förlust: −100 kr. Verifierad void:
  återbetald insats, netto 0 kr. Avbrott, walkover och andra specialfall
  kräver kontrollerad spelregel; osäker avräkning är `review` och förblir öppen.
- Summera vinster/förluster, utbetalningar och realiserat netto från hela
  loggen. ROI = netto / insatser på `won`/`lost`; exkludera void och öppna
  spel. Visa öppen insats separat. ROI och träffprocent saknas tills något
  spel avgjorts. Öppna spel har streck i utfallsfälten, inte en bokförd förlust.
- ”Visa saldo” betyder i nuläget resultatsaldo och öppen insats.
  Inget startkapital eller verkligt kontosaldo har fastställts.

## Senast verifierat läge

- Magnus bad ”rensa. Starta om”. Senaste nollställningen gjordes
  **22 oktober 2026 kl. 00.01 svensk tid**. Den tidigare serien med
  Cerúndolo, Mannarino och Nakashima finns i
  `tracking/archive/20261022T000128+0200/` och ingår inte i nya saldot.
  Återför inte äldre spel automatiskt från arkiv, analysfiler eller
  den separata serien i `atp-tennis-chat`.
- Aktuell serie: `atp-tennis-betting-20261022T000128+0200`.
  Två nya spel bokfördes kl. 00.04 efter analys av tolv matcher inom 24 timmar:
  - Tomáš Macháč mot Karen Khachanov, Almaty (`2026-9410`),
    ATP-ID `M0FH`/`KE29`, leverantörens match-ID `1029577805`.
    Låst odds **3,10**, TA **2,26**, insats **100 kr**.
    Planerad start 22 oktober kl. **10.00 svensk tid** (`08:00Z`).
  - Valentin Vacherot mot Luca Van Assche, Lyon (`2026-496`),
    ATP-ID `VA25`/`V0DZ`, leverantörens match-ID `1029570407`.
    Låst odds **1,62**, TA **1,42**, insats **100 kr**.
    Planerad start 22 oktober kl. **14.00 svensk tid** (`12:00Z`).
- Senaste resultatkontroll: **22 oktober 2026 kl. 00.12 svensk tid**.
  Båda matcherna var `NOT_STARTED` i direkt Svenska Spel-flöde, inga resultat
  i MariaDB. Öppen insats **200 kr**, noll avgjorda spel, realiserat netto
  **0 kr**. En plats är ledig. Detta är ett historiskt kontrolläge, inte
  aktuell status vid nästa läsning. Tiderna är preliminära.
- Magnus uppgav sedan att han själv satsat 100 kr på båda och bekräftade
  uttryckligen odds **3,10 och 1,62**. Bekräftelsen sparades kl. **00.18**
  i `user_reported_actual_bet`. Faktisk totalinsats är **200 kr**.
  Ingen ny resultatkontroll gjordes då. Påstå inte längre att Magnus bara
  har pappersspel; skilj hans bekräftade insatser från framtida rekommendationer.
- Läs alltid aktuell logg och senaste händelser ur `tracking/`.
  Urvalsunderlag: `analysis/20261022T000128+0200/assessment.md`.
  Senaste pingunderlag: `analysis/20261022T001252+0200/` och
  `tracking/checks/20261022T001252+0200.json`.
- Motiveringar vid bokföring: Macháč bedömdes subjektivt till cirka 37 %
  mot prisets nollpunkt 32,3 %, med lägsta spelgräns 2,85. Khachanov ansågs
  fortfarande mest sannolik vinnare. Vacherot bedömdes subjektivt till cirka
  66 % mot nollpunkten 61,7 %, spelgräns 1,58. Dessa är osäkra egna
  bedömningar, inte kalibrerade sannolikheter eller databasens GPT-odds.
  Magnus vill gärna ha motivering till avvikelser från marknadens odds.
- Den tredje platsen fylldes inte för kvotens skull. Nakashima valdes bort
  till aktuella 1,45 (ny subjektiv gräns 1,50). Övriga bortval finns i analysen.

## Affischer och e-post

- Senaste affischen för nya serien finns i
  `output/posters/20261022T000412+0200/tva-bokforda-spel.png`.
  Prompt och data ligger i samma katalog. Den visar två bokförda spel,
  en ledig plats och status från **22 oktober kl. 00.04**. Affischen
  skapades innan Magnus bekräftade verkliga insatser och beskriver därför
  spelen som simulerade. Vid ny affisch: skilj korrekt på bekräftade
  faktiska spel och eventuella nya pappersspel.
- Affischerna i `output/posters/20261021T223749+0200/` avser den gamla
  serien och ska inte visas som aktuella. Den senaste versionen av den
  gamla affischen skickades på Magnus uttryckliga begäran via Apple Mail
  till hans Gmail-adress; sändningen verifierades i Skickat. Ingen senare
  affisch har mejlats. Skicka inte fler mejl utan ny instruktion.
- Built-in imagegen användes för affischerna. Genererade projektbilder
  kopieras till projektets `output/posters/`, med sparad prompt och data.
