# ATP Tennis Betting

Separat projekt för bettingdelen från `atp-tennis-chat`.

## Datakällor

Använd inte `tennis.egelberg.se`: varken för data, som reservväg eller för
drift och schemaläggning. Använd den gemensamma skillen **atp-tennis** för all
databasåtkomst och hämtning av Svenska Spels odds. Skillen läser MariaDB och
hämtar odds direkt från leverantörsflödet utan webbläsare. Matchprogram, underlag
och färska resultat från ATP, arrangören eller Tennis Abstract.
Direktåtkomst till dessa externa källor måste verifieras innan de används.
Historiska filer behåller sin ursprungliga källangivelse, men snapshots från
den förbjudna tjänsten får inte återanvändas som nytt analysunderlag.

## Huvuduppgift

Kunna svara på: **”Vilka tre kommande matcher är värda att satsa på?”**

Målet är att över tid följa resultatet av egna matchanalyser med TA-odds som
vägledning. Urvalet ska bygga på en självständig bedömning av spelarnas chans
att vinna till erbjudet odds. Resultatet av serien utvärderar denna samlade
metod; det kan inte ensamt visa effekten av TA-modellen isolerat.

Svaret ska ge upp till tre motiverade singelspel i olika kommande ATP-matcher,
med matchstart i svensk tid, spelare, aktuellt Svenska Spel-odds, TA-odds,
bedömd lägsta spelgräns och viktigaste osäkerhet. Välj efter spelvärde vid
erbjudet odds och en samlad bedömning av matchen.

Arbetsgång:

1. Hämta aktuellt utbud med skillens `scripts/svenskaspel.py`. Använd
   huvudtourens herrsingel, verifiera underlag och båda ATP-ID och uteslut
   påbörjade matcher. Välj bara matcher med verifierad planerad start inom
   de närmaste 24 timmarna; gränsen räknas från bokföringstillfället,
   inte per kalenderdygn. Uteslut matcher utan verifierbar starttid.
   Ange vilka datum och matcher urvalet täcker.
2. Hämta endast TA-underlaget via skillens `scripts/database.py`; hoppa över databasens
   GPT-odds helt. `WIN_PROBABILITY_TA(A,B,surface)` ger marginalfri sannolikhet
   `p`. Motsvarande TA-pris är `ROUND(1 / LEAST(0.999, GREATEST(0.001, p * 1.05)), 2)`
   enligt databasens befintliga prissättning. För andra sidan används `1-p`.
   TA-oddsen inkluderar redan 5 % sannolikhetspåslag och jämförs direkt med
   Svenska Spels odds; lägg inte på ytterligare marginal. Undvik
   `PLAYER_ODDS`, som även beräknar GPT-oddsen.
3. Använd TA som vägledning, inte som ett mekaniskt urval efter största
   oddsgap. Om TA-modell-EV redovisas beräknas den med den marginalfria
   sannolikheten: `p * spelodds - 1`. Ett odds-prisgap är inte förväntad
   avkastning och TA-modellens sannolikhet är inte automatiskt egen bedömning.
4. Granska aktuell form, motståndets kvalitet, underlag och relevant fysisk
   information och analysera matchbilden. Komplettera med aktuella externa
   källor vid behov. Motivera val och osäkerhet självständigt; ett stort
   TA-gap räcker inte som rekommendation.
5. Välj högst en sida per match med positivt bedömt spelvärde enligt den egna
   analysen. TA-modell-EV är ingen obligatorisk urvalsgräns. Redovisa färre
   än tre spel om underlaget inte motiverar tre. Skilj modellvärden från egen
   bedömning och ange hur den bedömda spelgränsen har satts.
6. Kontrollera pris och matchstatus igen före svaret. Ange uttagstid,
   källor och databegränsningar. Spara oddsunderlag och beräkningar vid analys.

Historik och modellvärden läses direkt från databasen. Hämta kompletterande
turneringskalender och lottningar direkt från ATP, arrangören eller Tennis
Abstract. Saknas verifierade aktuella odds eller matchstatus ska detta
redovisas; ge inga nya tips baserade på gamla priser.

## Speluppföljning

Vi följer rekommendationerna som simulerade singelspel med 100 kr per match.
Tre löpande spelplatser fylls vid kommandot **”ping”**. Avräkna färdiga spel
och fyll lediga platser med nya kommande matcher; högst tre spel är öppna
samtidigt. Oförändrat läge ger en kort statusrapport, inga nya spel.
Låsta odds och insatser finns i `tracking/bets.json`; matchutfall och netto
sammanställs i [tracking/overview.md](tracking/overview.md).
Avräkningsregler och loggformat beskrivs i [tracking/README.md](tracking/README.md).
Uppföljningen görs vid manuellt ping och, på Magnus uttryckliga begäran den
22 oktober 2026, automatiskt var sjätte timme i denna chatt. Automationen
”ATP-ping var sjätte timme” kräver att Macen är vaken och uppkopplad med appen
igång eftersom filer och skills är lokala. Detta ersätter äldre uppgifter
om att ingen schemaläggning är aktiverad, även i sparad kontext.
Efter varje ping skickas en affisch via den gemensamma **pushover**-skillen
med rubriken ”Spelstatus” och platserna ”Spel 1”, ”Spel 2” och ”Spel 3”:
spelare, låst Svenska Spel-odds jämfört med TA-odds vid bokföringen,
diff i implicerad sannolikhet (procentenheter), insats och starttid eller
”Ledigt”. Nya spel markeras, pågående matcher visar tillgänglig ställning och
oklar status anges uttryckligen. Affischen visar också antal avgjorda matcher
och totalt antal bokförda spel i aktuell serie. Ingen separat textsammanfattning skickas;
Pushover kräver ett textfält, som enbart innehåller ”Spelstatus”.
Rutinen och skyddet mot dubbla
utskick beskrivs i `tracking/README.md`.

## Gemensamma verktyg

Databasanslutning, Svenska Spel-flöde, Python-beroenden och lokal konfiguration
hanteras av [atp-tennis-skill](https://github.com/meg768/atp-tennis-skill).
Skillen ska vara installerad som `~/.agents/skills/atp-tennis`; läs dess
`SKILL.md` och relevanta referenser före användning. Projektet har ingen egen
anslutningskod, `.env` eller Python-miljö.

Läs en SQL-fråga från standard input eller en fil med skillens Python:

```sh
echo 'SELECT 1 AS connection_ok;' | ~/.agents/skills/atp-tennis/.venv/bin/python ~/.agents/skills/atp-tennis/scripts/database.py
~/.agents/skills/atp-tennis/.venv/bin/python ~/.agents/skills/atp-tennis/scripts/database.py query.sql
```

Hämta aktuellt oddsunderlag utan webbläsare:

```sh
~/.agents/skills/atp-tennis/.venv/bin/python ~/.agents/skills/atp-tennis/scripts/svenskaspel.py
```

Skillens databasverktyg använder en lästransaktion. Vid saknad skill eller
utebliven datakontakt: redovisa felet. Skapa ingen lokal reservanslutning och
öppna inte Svenska Spel i webbläsaren som automatisk reservväg.

Spelurval, bokföring, avräkning och historik hör fortsatt till detta projekt.
Analyskatalogernas engångsskript anropar skillens verktyg och ska köras med
skillens Python om de behöver granskas. De innehåller historiska datum och
urval; kör inte gamla registreringsskript igen. Sparade analyser, rådata och
spelloggar är underlag för efteranalys och ska bevaras.

Äldre hänvisningar till projektets `scripts/database.py`, `.env` eller
`.venv` i sparad kontext och historiska rapporter avser den tidigare lösningen.
Använd alltid skillens verktyg enligt instruktionerna ovan.
