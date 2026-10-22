# Uppföljning av rekommenderade spel

Pappersportfölj med 100 kr per rekommenderad match. Detta är simulerade spel
till publicerade odds, inte bekräftade spel hos en speloperatör. Serien är
separat från den tidigare loggen i `atp-tennis-chat`.

Spelloggen nollställdes senast på Magnus uttryckliga begäran den 22 oktober 2026
kl. 00.01 svensk tid. Den tidigare serien finns i `archive/20261022T000128+0200/`
och ingår inte i den nya seriens saldo. Aktuellt innehåll finns i
`bets.json` och senaste avräkningarna. Återför inte gamla spel eller
kontrollhistorik automatiskt från arkivet eller gamla analysfiler. Äldre
affischer visar den tidigare serien.

## Ping och de tre spelplatserna

Magnus skriver ”ping” när uppföljning önskas. Kör ingen schemaläggning.
Använd enbart den gemensamma skillen `atp-tennis` för databasåtkomst och
Svenska Spels aktuella odds och matchstatus. Skillens verktyg och Python
finns under `~/.agents/skills/atp-tennis`; projektet har ingen egen anslutning.
Det finns högst tre samtidigt öppna spel, med 100 kr per spel. Urvalet bygger
på egna analyser med TA som vägledning.

**”Kommande” betyder ett redan bokfört pappersspel på 100 kr till låst odds.**
I rapporter ska statusen skrivas **”Spel bokfört – inväntar matchstart”**,
med insats och låst odds bredvid.
Platsen är upptagen och insatsen ingår i öppen insats redan före matchstart.
När matchen börjar ändras matchstatus till ”Pågående”; registrera inte ett
nytt spel och dra inte insatsen igen. En kandidat som ännu inte bokförts får
inte visas som ”Kommande” bland de tre spelplatserna.

1. Läs samtliga registrerade spel och senaste avräkningshändelse per spel.
   Ett spel utan avräkning är öppet. Kontrollera alla öppna matcher mot
   aktuella resultat och matchstatus.
2. Avräkna verifierat avgjorda spel och lägg till nya händelser. En pågående,
   kommande, uppskjuten eller ännu oklar match ligger kvar på sin plats.
   Även `review` upptar en plats tills avräkningen är klar.
3. Beräkna lediga platser som tre minus antalet öppna spel. Fyll dem vid
   samma ping med nya kommande matcher enligt egen matchanalys i projektets
   README. Nya spel måste ha verifierad planerad start efter bokföringstillfället
   och senast 24 timmar därefter, och matchen får inte ha börjat. Kontrollera
   tidsgränsen igen vid bokföringen. Saknas verifierbar starttid eller bra
   kandidater inom fönstret, låt platser stå tomma. TA är vägledning;
   använd inte databasens GPT-odds. Behåll
   befintliga öppna spel och deras låsta odds även om nya kandidater ser bättre ut.
   24-timmarsgränsen gäller bara nya spel; redan bokförda spel ligger kvar
   även om starttiden ligger längre fram eller flyttas utanför fönstret.
4. Lås nya val, odds, 100 kr insats, aktuell tidsstämpel, båda ATP-ID,
   turneringsupplaga, analys och källor före matchstart. Registrera aldrig
   samma matchspel igen. Använd ny aktuell `recommended_at` för nya val.
   Låt platser stå tomma om verifierade priser
   eller tillräckligt bra kandidater saknas; redovisa varför.
5. Visa kort de upp till tre öppna spelen med status kommande/pågående/
   uppskjuten/oklar, starttid i svensk tid, låsta odds och insats. Visa nya
   avräkningar med slutresultat och netto, motivera eventuella nya val och
   redovisa ackumulerat netto och öppen insats.

Om ett nytt ping kommer efter fem minuter och inget har ändrats: skapa inga
nya spel eller dubbla avräkningar. Visa bara kort aktuell status för befintliga
matcher och totalsumman. Dra inte slutsatsen att en match har börjat eller
slutat enbart för att den planerade starttiden har passerat; markera okänd
status när den inte går att verifiera. Vid utebliven datakontakt, ange senaste
verifieringstid i stället för att presentera gammal status som aktuell.

## Dubblettkontroll

Kontrollera varje ny kandidat mot **hela** `bets.json`, inklusive alla datum
och redan avgjorda spel. En match längre fram än morgondagen är redan bokförd
när den tilldelats en spelplats och får inte väljas igen när matchdagen närmar sig.

Matchidentiteten är turneringsupplagans `event_id` tillsammans med båda
ATP-ID i sorterad ordning. Samma match ska stoppas även om spelarsidorna
bytt plats, den andra spelaren föreslås, oddset ändrats, matchen flyttats
eller oddsleverantören gett den ett nytt event-ID. Kontrollera också
dubbletter inom det nya kandidatpaketet. Statusvisning av ett befintligt
spel medför aldrig en ny insats. Nollställ inte historiken vid dygnsskifte.

## Bokföring

- `bets.json`: låsta rekommendationer med unika spel-ID, båda ATP-ID,
  turneringsupplaga, ursprunglig starttid, odds och insats. Ändra inte historiska
  val eller odds och registrera inte samma matchspel igen.
  Valfritt `user_reported_actual_bet` på ett befintligt spel anger insats och
  odds som Magnus själv har placerat och uttryckligen bekräftat. Ändra inte
  pappersspelets ursprungliga priser eller registreringstid. Räkna inte
  bekräftelsen som ett nytt spel eller en ytterligare insats. Redovisa faktisk
  insats och resultat separat från pappersserien; använd bekräftade faktiska
  odds för verkligt resultat och tillämplig spelregel vid specialfall.
- `settlements.jsonl`: en avräkningshändelse per rad. Lägg till händelser;
  ersätt inte historiken. Senaste händelsen per spel gäller.
- `overview.md`: aktuell läsbar sammanställning som får uppdateras.

Sammanställningen ska innehålla **alla bokförda matcher**, även avslutade,
med vald spelare, motståndare, låst odds, insats, matchresultat, spelutfall
(vinst/förlust/void/öppet), utbetalning och netto i kronor. Avslutade matcher
ligger kvar i historiken när en spelplats fylls på. Öppna spel visas med
streck för utbetalning och netto, inte som nollresultat eller förlust.

## Historik för senare analys

Magnus vill kunna analysera alla spel i efterhand. Behåll varje bokfört spel
och dess ursprungliga tid, spelare, motståndare, turneringsupplaga, underlag,
låsta spelodds, TA-odds, insats, egen sannolikhetsbedömning och spelgräns,
motivering, risker och källor. Behåll tillhörande analysfiler och råunderlag.
Skriv inte om den ursprungliga bedömningen när resultatet blivit känt;
eventuell efteranalys ska vara separat och daterad.

Behåll resultat, utbetalning och netto för alla avslutade spel, inklusive
förluster och void. Alla resultatkorrigeringar ska vara spårbara i
`settlements.jsonl`. Vid en uttryckligt begärd nollställning ska den tidigare
serien arkiveras för analys och hållas skild från den nya seriens saldo.

Skilj alltid Magnus bekräftade faktiska spel från pappersspel när insatser,
träffprocent, ROI eller andra resultat analyseras. Begränsa analysen till den
efterfrågade serien eller perioden och ange antalet avgjorda spel. Diff mot
TA visas som skillnad i implicerad sannolikhet, i procentenheter:
`100 * (1 / TA-odds - 1 / låst spelodds)`. TA:s befintliga 5 % marginal
behålls; diffen är inte förväntad avkastning.

## Avräkning och verifiering

Avräkningshändelser ska innehålla `bet_id`, `checked_at`, `status`,
`match_status`, `score`, `winner_id`, `source`, `source_match_id` samt
`payout_sek` och `net_sek` när spelet är avgjort. Ange en förklaring vid
korrigering eller oklar avräkning. Status är `pending`, `won`, `lost`, `void`
eller `review`. Skapa inte dubbla händelser vid oförändrat utfall.

Matcha resultat med båda ATP-ID och rätt turneringsupplaga; kontrollera omgång
om flera matchkopplingar är möjliga. Eventdatum i databasen är turneringens
startdatum. Matchens försvinnande från ett live- eller oddsflöde bevisar inte
att matchen är avgjord. Läs i första hand MariaDB via atp-tennis-skillens
`scripts/database.py`,
och kontrollera officiella ATP- eller arrangörskällor när importen ligger efter.
Databasen används endast för läsning.

Använd inte `tennis.egelberg.se` för uppföljning eller schemaläggning.
Resultatkontroller görs direkt mot databasen eller officiell källa.

Vid normal färdigspelad match blir utbetalningen insats gånger låst odds vid
vinst, annars 0 kr. Netto är utbetalning minus insats. Använd `Decimal` och
avrunda penningbelopp till ören. Walkover, avbrott, diskvalifikation och andra
specialfall kräver kontrollerad tillämplig spelregel innan avräkning. Markera
oklara fall `review`. Bekräftad `void` återbetalar insatsen och ger netto 0 kr.
En pågående eller uppskjuten match förblir `pending`.

Summera utbetalningar och netto endast för avgjorda spel. Visa öppen insats
för `pending` och `review` separat. ROI är realiserat netto på `won`/`lost`
delat med deras insatser; `void` och öppna spel ingår inte i nämnaren.
Träffprocent är vinster delat med vinster plus förluster. Saknas avgjorda spel
är ROI och träffprocent ej beräkningsbara. Räkna om sammanställningen från hela
spelloggen och senaste avräkning, inte genom att addera gamla rapportsummor.

Det behövs ingen ständig livebevakning för resultatbokföringen: kontrollera
samtliga öppna spel vid nästa körning. Nya rekommendationer måste däremot
registreras före matchstart; skapa aldrig historiska tips i efterhand.

Ingen schemalagd uppföljning är aktiverad. Automationen ”Dagliga ATP-tips och
spelresultat” som kördes dagligen kl. 07.00 togs bort på Magnus begäran den
21 oktober 2026. Skapa inte en ersättare utan en ny instruktion från Magnus.
