# Kontroll av TA-odds för de fyra bokförda spelen

Kontroll gjord den 22 oktober 2026 från kl. 19.30 svensk tid. Omfattning:
samtliga fyra spel i aktuell serie, inklusive de två avslutade spelen.
Databasen användes endast för läsning. Historiska spelposter och avräkningar
har inte ändrats.

## Slutsats

Databasens metod stämmer med Tennis Abstracts dokumenterade Elo-formel för
bäst av tre set. Alla åtta lagrade hardcourt-Elo-värden motsvarar Tennis
Abstracts publicerade hElo-värden avrundade till heltal. Det finns ingen
större avvikelse i denna jämförelse, men heltalslagringen förlorar precision.

För de valda spelarna matchar tre av fyra bokförda TA-odds en omräkning från
webbplatsens hElo-värden med en decimal och projektets oförändrade 5 % marginal.
Vacherots odds blir **1,43** i stället för bokförda **1,42**.

| Spel på | Motståndare | Bokfört TA-odds | Omräknat från publicerat hElo, samma 5 % marginal | Skillnad i odds |
|---|---|---:|---:|---:|
| Tomáš Macháč | Karen Khachanov | 2,26 | 2,26 | 0,00 |
| Valentin Vacherot | Luca Van Assche | 1,42 | 1,43 | +0,01 |
| Adrian Mannarino | Nikoloz Basilashvili | 1,62 | 1,62 | 0,00 |
| Francisco Cerúndolo | Clément Chidekh | 1,21 | 1,21 | 0,00 |

Detta är omräknade odds från Tennis Abstracts offentliga underlag med
projektets marginal, inte ett påstående att Tennis Abstract publicerar
spelbolagsodds med denna marginal.

## Precision i Elo-underlaget

Tennis Abstracts senaste publicerade Elo-lista är daterad **19 oktober 2026**.
Värdena nedan är hämtade direkt från kolumnen hElo, inte hElo Rank eller
den övergripande Elo-kolumnen. hElo är redan Tennis Abstracts blandning av
övergripande och underlagsspecifik styrka; ingen extra blandning ska göras.

| Spelare | Publicerat hElo | Databasens elo_rank_hard |
|---|---:|---:|
| Tomáš Macháč | 1755,0 | 1755 |
| Karen Khachanov | 1810,4 | 1810 |
| Valentin Vacherot | 1830,8 | 1831 |
| Luca Van Assche | 1709,2 | 1709 |
| Adrian Mannarino | 1664,0 | 1664 |
| Nikoloz Basilashvili | 1603,3 | 1603 |
| Francisco Cerúndolo | 1839,9 | 1840 |
| Clément Chidekh | 1616,0 | 1616 |

Informationsschemat bekräftar att `elo_rank`, `elo_rank_hard`, `elo_rank_clay`
och `elo_rank_grass` har typen `INT`. Alla åtta undersökta värden matchar
heltalsavrundning av webbplatsens värden. Importkod har inte undersökts i
denna kontroll, så exakt var avrundningen sker i importkedjan är inte fastställt.

## Beräkning och återkontroll

Databasens faktiska definition av `WIN_PROBABILITY_TA` har lästs. För Hard
använder den `players.elo_rank_hard` och returnerar marginalfri sannolikhet:

```text
p = 1 / (1 + 10 ^ ((motståndarens hElo - spelarens hElo) / 400))
```

Projektets prissättning tillämpas därefter en gång:

```text
TA-odds = ROUND(1 / LEAST(0.999, GREATEST(0.001, p * 1.05)), 2)
```

För varje spel har både den sparade sannolikheten och det sparade TA-oddset
återskapats från databasens heltal. Ny läsning av databasfunktionen ger samma
sannolikhet inom 1e-12. De bokförda priserna är alltså korrekt återgivna från
databasen; precisionen i dess indata förklarar skillnaden mot omräkningen
från webbplatsens decimaler. Ingen GPT-oddsfunktion har anropats.

| Spelare | Sparad sannolikhet | Omräknad från publicerat hElo | Skillnad i procentenheter |
|---|---:|---:|---:|
| Macháč | 42,1503 % | 42,0942 % | +0,0561 |
| Vacherot | 66,8695 % | 66,8185 % | +0,0510 |
| Mannarino | 58,6895 % | 58,6476 % | +0,0419 |
| Cerúndolo | 78,4054 % | 78,3956 % | +0,0097 |

Även båda sidor av varje match har jämförts. Små avvikelser på motståndarsidan
framgår av `comparison.json`: Khachanov 1,65 i databasen mot 1,64 från
decimalerna; Basilashvili 2,31 mot 2,30. Van Assche 2,87 och Chidekh 4,41
är oförändrade.

## Kontroll mot publicerade turneringsprognoser

De offentliga turneringssidornas HTML innehåller JavaScript-variabeln
`projCurrent`. Relevant tabell har lästs direkt ur HTML utan att exekvera
JavaScript eller gå via någon annan tjänst. För de fyra matcherna visar
prognoserna följande avrundade sannolikheter för vald spelare:

- Almaty: Macháč 42,1 % i QF-kolumnen mot Khachanov; Mannarino 58,7 % i
  SF-kolumnen mot Basilashvili, efter 100 % i QF-kolumnen.
- Lyon: Vacherot 66,8 % i QF-kolumnen mot Van Assche.
- Bryssel: Cerúndolo 78,4 % i SF-kolumnen mot Chidekh, efter 100 % i
  QF-kolumnen.

Sidorna beskriver prognoserna som turneringssimuleringar med underlagsspecifik
Elo och visar avrundade procenttal. Dessa ger en kompletterande rimlighetskontroll,
inte ytterligare exakta decimaler att prissätta efter. Prognossidornas
publicerade omgångsläge får inte användas som aktuell matchstatus: de hämtade
tabellerna innehåller fortfarande Macháč och Vacherot som förhandsprognoser.

## Praktisk följd

För närmare överensstämmelse med det publicerade underlaget bör Elo lagras
med minst en decimal och avrundning av oddset göras först efter
sannolikhetsberäkningen och marginalen. En sådan ändring av databas och
import kräver separat uttrycklig instruktion från Magnus. Den här kontrollen
ändrar inte databas, schema, import eller låsta historiska värden.

Kontrollen gäller tillgänglig offentlig Elo-lista och de sparade
databasvärdena. Den hämtade sidversionen är inte ett oberoende historiskt
webbarkiv från varje exakt bokföringstillfälle. Fullständiga, opublicerade
interna TA-ratingdecimaler kan inte verifieras här.

## Källor och sparat underlag

- [Tennis Abstract: ATP Elo Ratings](https://www.tennisabstract.com/reports/atp_elo_ratings.html)
- [Tennis Abstract: An Introduction to Tennis Elo](https://www.tennisabstract.com/blog/2019/12/03/an-introduction-to-tennis-elo/)
- [Almaty: Results and Forecast](https://www.tennisabstract.com/current/2026ATPAlmaty.html)
- [Lyon: Results and Forecast](https://www.tennisabstract.com/current/2026ATPLyon.html)
- [Brussels: Results and Forecast](https://www.tennisabstract.com/current/2026ATPBrussels.html)
- `database-audit.json`: läst funktionsdefinition, datatyper och databasvärden.
- `tennisabstract-elo.html`, `tennisabstract-elo-rows.json`: källsida och relevanta Elo-rader.
- `tennisabstract-almaty.html`, `tennisabstract-lyon.html`, `tennisabstract-brussels.html`:
  hämtade turneringssidor.
- `tennisabstract-forecast-rows.json`: relevanta rader från prognostabellerna.
- `comparison.json`: samtliga beräkningar, precision och priser på båda spelarna.
