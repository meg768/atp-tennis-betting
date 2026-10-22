# Ny serie – urval inom 24 timmar

Magnus bad den 22 oktober 2026 att rensa och starta om. Den tidigare serien har arkiverats, inklusive kontrollhistorik, och ingår inte i det nya saldot. Gamla affischer gäller den tidigare serien.

12 ännu ej påbörjade ATP-singelmatcher hade öppna matchvinnarmarknader och planerad start inom de närmaste 24 timmarna vid det första uttaget strax efter midnatt svensk tid. Matchernas kalenderdag och underlag stöds av officiella spelscheman. Nytt pris, öppen marknad, matchidentitet, status och 24-timmarsgräns kontrolleras igen vid registreringen.

TA är vägledning. Ingen GPT-oddsfunktion har anropats. TA-priserna har redan 5 % marginal. Egna sannolikheter och spelgränser är subjektiva bedömningar, inte en kalibrerad modell eller TA:s sannolikheter.

## Bortval

- Nakashima–Jacquet: Nakashima är fortsatt favorit. Men priset har fallit till 1,45, Jacquet har vunnit sju av sina tio senaste registrerade matcher inklusive kval och slog Berrettini i två set. Jag kräver nu minst 1,50 för att kompensera för osäkerheten. Matchen återförs inte från den gamla serien.
- Altmaier–Gojo: TA-gynnsamt pris på Altmaier räcker inte. Hans registrerade hardcourt-facit 2026 är 5–13 mot Gojos 32–11 inklusive kval och lägre turneringsnivåer. Gojo har dessutom tre vinster i Lyon. Ingen vald sida.
- Goffin–Michelsen: största modellgapet på Goffin, men 2–8 senaste tio registrerade och 0–6 på hardcourt 2026 före hans färska Brysselseger. Michelsen 27–13 på hardcourt och enkel öppningsseger. Den färska segern mot Bertola verifieras i officiell lottning men undanröjer inte osäkerheten.
- Dzumhur–Bergs: Dzumhurs Olbia-titel är främst Challenger-underlag; Bergs slog Alcaraz i Shanghai och har starkare aktuella ATP-meriter. Inget spel trots positiv TA-screening.
- Atmane–Bellucci: två nyliga avbrott i Atmanes registrerade historik, Bellucci 9–1 på senaste tio registrerade. Det måttliga TA-gapet räcker inte.
- Övriga matcher: underlaget gav ingen tydligare egen fördel än de två valda spelen. Fyll inte den tredje platsen för kvotens skull.

## Begränsningar och underlag

MariaDB lästes direkt via scripts/database.py. Databasen ligger efter på en del aktuella matcher. Exempelvis saknas Macháč–Nurlanuly i uttaget men arrangörens schema visar 6–2, 6–0. Senaste-tio- och årsstatistik inkluderar alla registrerade nivåer och kval samt Completed/Aborted, inte Walkover. Turneringens datum är inte matchdatum; omgångsordning används inom samma turnering. Rankningar i databasen och lottningarnas seedningslistor kan avse olika uttag. Ingen fullständig skadebild eller särskild inomhusmodell har verifierats.

ATP:s live-API gav en Cloudflare-sida vid detta uttag. Svaret är sparat som atp-live-error.html och har inte använts som matchdata. Officiella spelscheman och lottningar samt arrangörens resultatsida kompletterar databasen. Preliminära starttider från Svenska Spels leverantörsflöde används i loggen.

## Källor

- MariaDB: WIN_PROBABILITY_TA, players, matches, events.
- Svenska Spels direkta leverantörsflöde: svenskaspel-raw.json och final-odds-check.json.
- https://almatyopen.ktf.kz/en/schedule
- https://www.protennislive.com/posting/2026/9410/op.pdf
- https://www.protennislive.com/posting/2026/496/mds.pdf
- https://www.protennislive.com/posting/2026/496/op.pdf
- https://www.protennislive.com/posting/2026/7485/mds.pdf
- https://www.protennislive.com/posting/2026/7485/op.pdf

Reproducerbart underlag: screening.json, profiles.json, recent.json, recent-query.sql, recent-params.json, head-to-head.json. register.py får inte köras igen för att skapa dubbletter.

## Tomas Machac mot Karen Khachanov

Macháč är outsider, men 3,10 kräver bara cirka 32,3 % vinstchans. Hardcourt-Elo 1755 mot Khachanovs 1810 talar för en mindre nivåskillnad än oddsen antyder. Macháč vann första omgången 6–2, 6–0 enligt arrangören. Jag bedömer hans chans till ungefär 37 %, försiktigare än TA:s cirka 42 %, och kräver minst 2,85 för att ha viss marginal till osäkerheten.

Risk: Khachanov är rättmätig favorit: 7–3 på de senaste tio registrerade matcherna mot Macháčs 4–6 före den färska Almatysegern. Khachanov slog Sakamoto 6–2, 6–4 och vann deras enda registrerade inbördes möte. Macháčs lätta öppningsmotstånd bevisar inte toppform. Ingen fullständig aktuell skadebild har verifierats.

## Valentin Vacherot mot Luca Van Assche

Vacherots hardcourt-Elo är 1831 mot Van Assches 1709. De registrerade Tokyo-segrarna över Fils och Tsitsipas visar att han kan prestera mot starkt motstånd. Jag bedömer cirka 66 % vinstchans, försiktigare än TA:s cirka 67 %, jämfört med prisets nollpunktskrav på cirka 61,7 %. Ett subjektivt rättvist odds runt 1,52 motiverar spel först från 1,58; erbjudna 1,62 ger en mindre men tillräcklig marginal.

Risk: Van Assche har 26–11 på registrerade hardcourt-matcher 2026 och vann Lyonöppningen i två set. Vacherot har förlorat två av sina tre senaste registrerade matcher och går in efter bye. Elo skiljer inte mellan hardcourt inne och ute. Spelet har begränsad marginal och bedömningen är subjektiv.
