# Ping 22 oktober 2026 kl. 16.20 svensk tid

## Avräkning

Direkt ATP-live-API visar normala färdigspelade matcher, status F, utan avbrottsorsak:

- Almaty 2026, MS011, ATP-ID M0FH/KE29: Khachanov vann. Från Macháčs sida: 2–6, 6–4, 6–7(7). Utbetalning 0 kr, netto −100 kr.
- Lyon 2026, MS010, ATP-ID VA25/V0DZ: Van Assche vann. Från Vacherots sida: 6–2, 4–6, 4–6. Utbetalning 0 kr, netto −100 kr.

MariaDB saknar ännu dessa resultat. De har verifierats med rätt år, turnering, båda ATP-ID, slutstatus, vinnare och setställning direkt från ATP; försvinnande från oddsflödet används inte som resultatbevis. Båda är även Magnus bekräftade faktiska spel med samma odds och insats, varför faktiskt realiserat netto är −200 kr och faktisk öppen insats 0 kr.

Mannarino–Basilashvili är fortfarande NOT_STARTED, preliminärt 23 oktober kl. 08.30 svensk tid. Det är befintligt pappersspel till 2,18 och registreras inte på nytt.

## Nytt val: Francisco Cerúndolo mot Clément Chidekh

Bryssel 2026, ATP-ID C0AU/C0BH, leverantörens match-ID 1029581066. Preliminär start 23 oktober kl. 14.00 svensk tid, bekräftad i officiellt fredagsprogram. Nuvarande 1,56 kräver cirka 64,1 % vinstchans. TA-pris 1,21, underliggande marginalfri TA-sannolikhet cirka 78,4 %.

Egen bedömning: Cerúndolo har den starkare etablerade nivån och hardcourt-Elo 1840 mot 1616. Aktuellt registrerat hardcourt-facit är 17–11 med bland annat segrar över Mensik och Safiullin. Han slog Damm 6–4, 7–6(4) i Bryssel. Jag bedömer ungefär 69 % vinstchans, tydligt försiktigare än TA. Det motsvarar rättvist odds omkring 1,45. Min subjektiva lägsta spelgräns sätts till 1,50 för viss marginal till osäkerheten; 1,56 är spelbart för 100 kr i pappersserien.

Risk: Chidekh är 9–1 på de senaste tio registrerade matcherna och har vunnit fyra raka matcher i Bryssel utan setförlust inklusive kval. Segrarna över Van de Zandschulp 6–1, 6–4 och Fearnley 7–6(4), 6–2 ger konkret stöd för att hans faktiska aktuella nivå kan överstiga långtidsmodellen. Detta är därför ingen säker favorit och TA:s cirka 78 % används inte som egen sannolikhet.

Den tidigare serien är nollställd och arkiverad; ingen gammal post återförs automatiskt. Valet bygger på nytt pris, färsk databas och nu godkänt 24-timmarsfönster. Full dubblettkontroll görs mot alla spel i den aktuella serien, inklusive de nyss avgjorda spelen. Nya rekommendationer är pappersspel tills Magnus bekräftar faktisk insats.

## Återstående plats lämnas ledig

- Lehečka–Griekspoor: Lehečkas hardcourt-Elo 1921 mot 1741 och Tokyo-final stöder favoritskapet. Han slog Collignon 6–4, 6–2 i dag enligt officiell lottning. Griekspoor har två vinster i Bryssel, men behövde tre jämna set mot Schoenhaus. Ändå är 1,43 ett tunt pris mot en stark servare. Egen grov uppskattning cirka 72 % innebär endast omkring 3 % villkorad avkastning till 1,43. Jag kräver minst 1,47 för bättre marginal till osäkerheten och avstår här. TA är 1,29; ett positivt TA-gap räcker inte.
- Nakashima 1,46 förblir under min subjektiva gräns 1,50. Jacquet har stark aktuell form. Inget spel.
- Dzumhur 4,10 har tidigare granskats och osäkerheten mot Bergs kvarstår. Lägre turneringsnivåer i den fina resultatserien försvårar en säker egen uppskattning. Inget spel.
- Fritz 1,19 kräver cirka 84 % vinstchans mot Herbert som är inne i turneringen efter tre vinster. Underlaget ger inte tillräcklig marginal; avstå. Marozsan–Bublik, Cobolli–Wawrinka, Moutet–Paul och Tsitsipas–Duckworth ger inte heller tillräckligt tydligt eget spelvärde vid dessa priser. Ingen extra insats bara för att fylla tre platser.

## Underlag och mått

Tio ännu ej påbörjade ATP-singelmatcher inom 24 timmar screenades direkt från Svenska Spels leverantörsflöde. Ny kontroll av odds, öppen marknad, startfönster och status krävs vid bokföringen.

- Direkt MariaDB: WIN_PROBABILITY_TA, players, events, matches. TA-priserna har redan 5 % marginal; ingen extra marginal tillkommer och inga GPT-odds anropades.
- Egen sannolikhet och spelgräns är subjektiva, inte en kalibrerad modell. Senaste-tio/årsfacit omfattar alla registrerade nivåer och kval, Completed/Aborted, inte Walkover. Hardcourt-Elo skiljer inte inne och ute. Ingen komplett aktuell skadebild har verifierats.
- När diff mot TA visas ska den enligt Magnus jämförelse med sin vy vara skillnad i implicerad sannolikhet, i procentenheter: (1/TA-odds − 1/spelodds) × 100. Behåll TA:s befintliga marginal. Detta är varken relativ oddsskillnad eller förväntad avkastning.
- Källor: svenskaspel-raw.json, final-odds-check.json, status.json, atp-live-response.txt, atp-live-raw.json, atp-live.json, new-settlements.json, screening.json, profiles.json, recent.json, recent-query.sql och recent-params.json.
- https://app.atptour.com/api/v2/gateway/livematches/website?scoringTournamentLevel=tour
- https://www.protennislive.com/posting/2026/7485/mds.pdf
- https://www.protennislive.com/posting/2026/7485/op.pdf
- https://www.protennislive.com/posting/2026/496/op.pdf
