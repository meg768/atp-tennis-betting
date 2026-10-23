# Schemalagt ping 23 oktober 2026 – slutkontroll kl. 18.44 svensk tid

## Avräkning

Cerúndolo vann mot Chidekh 6–2, 6–4, verifierat visuellt i ATP:s officiella huvudlottning för Bryssel 19–25 oktober 2026, upplaga 2026-7485. Spelaridentiteter C0AU/C0BH kontrollerade i databasen. PDF visar Cerúndolo vidare till semifinal med normalt färdigspelat resultat, utan avbrott eller walkover. Sparad PDF, renderad bild och atp-result-verification.json är underlag. MariaDB saknade ännu resultatet kl. 18.14. ATP:s live-API gav HTML och användes inte som data. Insats 100 kr till ursprungligt låst odds 1,56: utbetalning 156 kr, netto +56 kr. Detta är ett pappersspel utan bekräftad faktisk insats. Ny avräkning läggs till en gång.

## Öppet spel

Van Assche–Musetti är NOT_STARTED utan live-data i slutkontrollen kl. 18.44. Match-ID, båda namn och Lyon är verifierade. Preliminär start 20.10 svensk tid. Låst odds 2,90, TA 2,37 och insats 100 kr behålls. Aktuellt 2,95 ändrar inte den historiska insatsen. Ingen ytterligare insats eller ny rekommendation för samma match.

## Kandidatgranskning

Ny screening via atp-tennis-skillen kontrollerade ATP-ID, namn, hardcourt-Elo, TA-sannolikheter, öppna matchvinnarmarknader och start inom 24 timmar. Jämförelse mot hela seriens fem matcher med upplaga och sorterade ATP-ID. Van Assche–Musetti är redan bokförd. Påbörjade matcher utesluts. Inga GPT-odds används.

- Fils–Michelsen: 1,50/2,55 vid första uttaget. Fils 7–3 på de senaste tio färdigspelade matcherna och hardcourt-Elo 1961 mot 1836, men har inte spelat i Bryssel efter bye och walkover. Michelsen har två färska raka-set-vinster. TA:s cirka 67,3 % för Fils ger bara liten marginal mot 66,7 %-kravet; egen osäkerhet om matchform lämnar ingen tydlig prisfördel. Vid slutkontrollen har matchen STARTED och är därmed inte längre tillåten som nytt spel.
- Cobolli–Nakashima 2,65/1,48: Nakashima har högre hardcourt-Elo (1868 mot 1790), bättre importerad hardcourt-form och två Lyonvinster. Cobolli vann över Wawrinka i raka set och kan vara konkurrenskraftig, men kräver 37,7 % vid 2,65; en egen försiktig bedömning omkring 36–38 % ger ingen robust buffert. Nakashima behöver 67,6 %, medan min bedömning inte ligger tydligt över detta och TA ger cirka 61 %. Inget spel på någon sida.
- Struff–Bergs 2,70/1,46: båda 6–4 på senaste tio färdigspelade och två Brysselvinster. Struffs serve kan hålla matchen jämn, Bergs har hemmaplan och starkare längre hardcourt-Elo (1755 mot 1667). Struff behöver 37,0 %; en egen bedömning ungefär 36–38 % lämnar ingen tillräcklig buffert. Bergs 68,5 %-krav är för högt för min försiktiga bedömning. TA 37,6/62,4 % är referens, inte självständig rekommendation. Inget spel.
- Basilashvili–Tsitsipas 3,00/1,38, Almaty 24 oktober kl. 12.00 svensk tid: ny match inom 24 timmar, ej en dubblett av Mannarino-spelet. Tsitsipas har stor Elo-fördel 1855–1603, 8–2 på senaste tio importerade färdigspelade matcher och vann enligt färsk officiell lottning över Duckworth 6–3, 6–4. Basilashvili har fem raka Almatyvinster inklusive kval efter dagens 6–3, 6–1 mot Mannarino; dagens resultat saknas ännu i DB:s lokala matchlista. Hans aktuella nivå förefaller högre än den långsiktiga modellen. TA ger Tsitsipas cirka 81,0 %, men jag justerar försiktigt till ungefär 70–72 % med hänsyn till motståndarens starka vecka och modellens begränsningar. Det når inte tydligt över 72,5 %-kravet vid 1,38. Motsvarande cirka 28–30 % för Basilashvili når inte 33,3 %-kravet vid 3,00. Inget spel. Intervallen är subjektiva, okalibrerade bedömningar.

De två lediga platserna lämnas tomma. Ingen kvotfyllnad, inga retroaktiva spel. Alla kandidatpriser/status kontrollerades igen 18.44. Starttider är preliminära. Formfacit avser Completed och alla importerade turneringsnivåer inklusive kval. Walkover/avbrott hålls separat. DB-import kan ligga efter; eventdatum är turneringsstart, inte enskild matchdag. Ingen fullständig aktuell skadebild eller separat inomhusmodell har verifierats. TA-priser har redan 5 % marginal. Tidigare analyser och låsta bedömningar skrivs inte om.

## Sammanställning

Pappersserien: 1 vinst, 3 förluster, 4 avgjorda matcher av 5 bokförda, utbetalning 156 kr, realiserat netto −244 kr, öppen insats 100 kr, ROI −61 %, träffprocent 25 %. Bekräftade faktiska spel: netto −200 kr, öppet 0 kr. Summorna ska inte adderas. Historik bevaras och affisch skapas med inbyggda imagegen, granskas och skickas via Pushover-skillen. Ingen commit eller push.

Källor: svenskaspel-raw.json och final-odds-check.json via skillen; screening.json och recent.json med SQL/parametrar; officiella brussels-draw.pdf, lyon-draw.pdf, almaty-draw.pdf; atp-result-verification.json och settlement-identities.json. Resultatkälla https://www.protennislive.com/posting/2026/7485/mds.pdf. Kompletterande lottningar https://www.protennislive.com/posting/2026/9410/mds.pdf och https://www.protennislive.com/posting/2026/496/mds.pdf.
