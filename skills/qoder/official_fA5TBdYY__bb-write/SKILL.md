---
name: bb-write
description: TRIGGER bij het schrijven of substantieel herzien van een BeeHaive Building Block (`frontend/src/content/building-blocks/*.mdx`) of Guardrail (`frontend/src/content/guardrails/*.mdx`). Dwingt schrijfstijl-bb-conventies (em-dash-regel, koppen-toets, vetgedrukt+`:`, business-NL, drie-niveau Quick Start) af vóór de eerste Write/Edit-call op een BB- of GR-bestand.
type: capability
disable-model-invocation: false
---

# /bb-write — BB/GR-content schrijven volgens schrijfstijl-bb

Deze skill is een *forcing function* op de stijlgids in `~/ODIN/projecten/BeeHaive/.claude/schrijfstijl-bb.md`. De gids zelf is uitgebreid (330+ regels); deze skill condenseert de regels die in elke schrijf-sessie consequent fout gaan, en eist een pre-write-scan voordat Write of Edit wordt aangeroepen.

**Waarom deze skill bestaat:** de gids alleen lezen blijkt niet voldoende. Em-dashes, vetgedrukte koppen met `—` ipv `:`, en abstracte koppen (`-architectuur`, `-engine`, `-pijplijn`) sluipen in eerste-concept-tekst en moeten anders in een lees-review handmatig worden gerepareerd. De gids §8 noemt dit zelf als blinde vlek: *"em-dashes zijn in Engelstalige training diep ingebakken; ze sluipen terug in voorstellen die je zelf aanbiedt terwijl je de regel uitlegt"*.

## Wanneer deze skill triggert

- Schrijven of grondig herzien van `frontend/src/content/building-blocks/*.mdx` of `frontend/src/content/guardrails/*.mdx`
- Een nieuwe BB/GR uitbouwen via het 5-stappen-ritme (stap 3 in BB werkritme)
- Lees-review van bestaande BB/GR-content
- Niet voor: kleine typo-fixes, single-property-frontmatter-updates, of niet-content-bestanden

## Stap 1: Lees de gids en ken het BB-skelet

**Verplicht vóór schrijven:**

1. Lees `~/ODIN/projecten/BeeHaive/.claude/schrijfstijl-bb.md` integraal. De gids heeft 18 secties; ken minimaal §1, §4, §8, §10, §13, §14, §17, §18.
2. Lees twee tot drie referentie-pagina's als template-voorbeeld:
   - `frontend/src/content/building-blocks/knowledge.mdx` (volledige, gereviewde BB met 7 BBDisclosures)
   - `frontend/src/content/building-blocks/dynamic-context.mdx` (de baseline-BB-pagina)
   - `frontend/src/content/guardrails/robustness.mdx` (de baseline-GR-pagina, als je een GR schrijft)
3. Voor de te schrijven BB/GR: bekijk welke KnowledgeItems er in `backend/app/graph/seed.py` aan gekoppeld zijn — die geven de inhoudelijke ankers.
4. **Stel een terminologie-decision-log op** voor de pagina (zie Stap 1b). Doe dit *voordat* je begint met schrijven, niet halverwege.

## Stap 1b: Terminologie-decision-log

Inconsistente terminologie binnen één pagina ontstaat structureel: in eerste-conceptzinnen sluipen Engelse terminologie en NL-vertalingen door elkaar (`stream` naast `waarde-stroom`, `playbook` naast `werkboek`, `flow` naast `stroom`). De schrijfstijl-bb §12 (consistente terminologie binnen één pagina) wordt anders pas tijdens lees-review afgedwongen, met handmatige reparatie als gevolg.

**Verplichte stap vóór de eerste body-zin:**

1. Inventariseer de centrale Engelse vakterm(en) van de pagina. Voorbeelden per BB:
   - BB_02 (Client Blueprint): *value stream*, *workflow*, *playbook*, *prototype*, *value proposition*, *job-to-be-done*
   - BB_03 (Dynamic Context): *retrieval*, *chunking*, *context window*, *staleness*, *embedding*
   - BB_04 (Prompt Design): *system prompt*, *few-shot*, *chain-of-thought*, *iterative gesprek*

2. Voor elke vakterm: kies één gehanteerde NL-vorm en houd die vast. Schrijf de keuze op in een korte tabel — in de eigen scratch-buffer of als hidden HTML-comment in de MDX-frontmatter (top-of-file). Bijvoorbeeld voor BB_02:

   | Engelse term | Gehanteerde NL-vorm |
   |--------------|---------------------|
   | value stream | waarde-stroom (met koppelteken; samenstellingen waarde-stroom-niveau, waarde-stroom-eigenaar) |
   | playbook | playbook (ingeburgerd; geen vertaling) |
   | prototype | prototype (ingeburgerd) |
   | value proposition | value proposition (Engelstalig in productlogica-context, anders 'waarde-belofte') |
   | workflow | werkstroom |

3. Hanteer de canonieke parenthese-regel: bij **eerste vermelding** in de body de Engelse term tussen haakjes naast de NL-term: *"Een waarde-stroom (value stream) is..."*. Daarna alleen de NL-vorm.

4. **Uitzonderingen** zijn het waard te noteren:
   - Letterlijke citaten in de oorspronkelijke taal (Engels) blijven Engels.
   - Framework-eigennamen (bijv. *Product Value Stream* als unFIX-typenaam, *Operational Value Stream* in SAFe-context) blijven Engels.
   - Bij eerste check, geef expliciet aan of een term ingeburgerd is in NL business-taal (bijv. *prototype*, *playbook*, *MCP*, *RAG*) of vertaald moet worden.

**Test halverwege schrijven**: pak de term-tabel erbij. Heb je consequent dezelfde NL-vorm gebruikt? Zo niet, herstel onmiddellijk.

## Stap 1c: Begrippenlijst-vooraf-scan

Een veelvoorkomend patroon: tijdens schrijven worden vakbegrippen gebruikt die nog niet in `frontend/src/data/begrippen.ts` staan, en die later achteraf moeten worden toegevoegd. Aanleiding: bij `model-engines.mdx` werden 13 begrippen alsnog toegevoegd (LLM, frontier-model, redeneer-model, multimodaal, wereld-model, diffusiemodel, embedding-model, klassieke-ml, open-weight-model, tier, drift, tokenizer, SDK).

**Verplichte stap vóór de eerste BBDisclosure-zin:**

1. Inventariseer alle vakbegrippen die op deze pagina vermoedelijk vallen. Onderverdeel in:
   - **Bestaat al in `begrippen.ts`** → bij eerste vermelding per BBDisclosure linken via `[term](/begrippen#slug)`.
   - **Bestaat nog niet** → eerst entry toevoegen aan `begrippen.ts` met categorie + uitleg + `zieOok`. Pas daarna in body gebruiken.
2. Voor de te schrijven BB: open `begrippen.ts` en grep op verwachte slug. Als er geen treffer is, voeg een nieuwe entry toe vóór de eerste body-Write.
3. Documenteer in de term-tabel uit Stap 1b ook **of de term al in de begrippenlijst staat** (kolom "Glossary-slug").

## Stap 1d: Harde-claims-research-pakket

In de BB-pagina's komen claims voor over benchmarks, prijzen, releasedata, marktposities en "enige/eerste/grootste"-uitspraken. Vertrouwen op model-kennis is hier risicovol: bij `model-engines.mdx` was ongeveer een derde van alle harde claims in eerste concept achterhaald, eenzijdig of fout (factor 1.250 prijsverschil, "enige open-weight challenger", break-even-claim, GPT-5.5 release-context, Mistral Large 3 vs frontier, ontbrekende wereld-modellen).

**Verplichte stap vóór commit van een BB:**

1. Maak een lijst van alle **harde claims** in het concept. Categorieën:
   - Benchmarks en scores (SWE-Bench, GPQA Diamond, MMLU, etc.)
   - Prijzen per model en per token
   - Releasedata van modellen of frameworks
   - Marktposities ("eerste", "enige", "grootste")
   - Wettelijke deadlines en compliance-data (EU AI Act, etc.)
   - Numerieke uitspraken over volume, reductie, factor-X
2. Per claim: noteer de bron of "te verifiëren". Voor "te verifiëren": delegeer naar een research-agent vóór commit, niet ná publicatie.
3. Bij elke "enige/eerste/grootste"-claim hardop afvragen: ken ik de uitzonderingen? Heb ik daadwerkelijk uitgesloten dat er meer zijn?
4. Voor numerieke claims (factor X, percentage Y) een sanity-check uitvoeren: kloppen de getallen met de modellen die elders op dezelfde pagina staan?
5. **Wettelijk-artikel-precisie**: bij elke citatie van een EU AI Act-artikel (of andere wetgeving): verifieer dat het genoemde artikel daadwerkelijk de operationele eis bevat, niet alleen de capaciteit. Veelgemaakte fout: Art. 12 (record-keeping *capability* — wat gelogd moet kunnen worden) wordt geciteerd voor de 6-maanden retentieplicht, terwijl die staat in Art. 19 lid 1 (providers) en Art. 26 lid 6 (deployers). *Capability-artikelen* (wat moet het systeem kunnen) zijn niet hetzelfde als *operationele artikelen* (hoe lang bewaren, door wie, in welke vorm). Bij twijfel: lees de exacte artikeltekst op `artificialintelligenceact.eu` of `eur-lex.europa.eu`, niet alleen een secundaire toelichting. (Aanleiding: BB_05 Tool Integration citeerde Art. 12 voor de 6-maanden retentie in zowel checklist als evidence; correctie naar Art. 19.)

## Stap 2: Hard rules die altijd gelden

Deze drie regels worden in elke sessie geschonden als ze niet expliciet worden afgedwongen. Houd ze tijdens het schrijven actief op je netvlies.

### Regel 1: Geen losse em-dashes (` — `) in NL-tekst

Em-dashes mogen alleen in *paren rond een tussenzin*. Een enkele em-dash in een zin is bijna altijd fout in Nederlands.

- ✗ `het patroon blijft — het is een structurele eigenschap`
- ✓ `het patroon blijft: het is een structurele eigenschap`
- ✗ `**Tier 2 — Hoog risico**: ...`
- ✓ `**Tier 2, hoog risico**: ...`
- ✓ `Chroma's onderzoek testte 18 frontier-modellen — inclusief GPT-4.1, Claude Opus 4, Gemini 2.5 Pro — en vond dat...` (dubbele em-dash, OK)

**Vervangingsstrategie**, in volgorde van voorkeur:
1. `:` als het tweede deel het eerste expliciteert
2. `;` als het twee gelijkwaardige zinsdelen zijn
3. `,` of `(...)` voor een korte toevoeging
4. Zin opbreken met `.`

**Uitzondering:** Engelstalige citaten in het origineel mogen em-dashes bevatten.

### Regel 2: Na vetgedrukt onderwerp hoort `:`, geen `—`

In bullets, alinea-openers en tabelkoppen: vet-onderwerp + definitie scheidt door `:`.

- ✗ `**Systeeminstructies & rol-definities** — wie is de agent...`
- ✓ `**Systeeminstructies & rol-definities**: wie is de agent...`

### Regel 3: Koppen in gewone-woorden-toets

Vermijd samenstellingen met `-architectuur`, `-engine`, `-tijdperk`, `-pijplijn`. Een kop moet begrijpelijk zijn zonder de sectie zelf te lezen.

- ✗ `Retrieval-architecturen: van simpele RAG naar context engines`
- ✓ `Documenten ophalen: van simpel zoeken naar een intelligente zoekmachine`

### Regel 4: Geen calques (woorden die NL líjken maar het niet zijn)

Letterlijke vertalingen van Engelse woorden die grammaticaal correct lijken maar geen levend NL-woord zijn. Passeren spell- en stijlchecks; worden alleen gevangen door lezerstest. Volledige groei-lijst en achtergrond: `schrijfstijl-bb.md` §1b.

Bevestigde calques om vooraf te grep'en:

- ✗ `tegengift` (calque van *antidote*) → ✓ `tegenmaatregel`, `remedie`, `oplossing`
- ✗ `handcureren` / `hand-cureren` (calque van *to hand-curate*) → ✓ `handmatig samenstellen`
- ✗ `kwartaal-cadans` (calque van *quarterly cadence*) → ✓ `elk kwartaal`, `eens per kwartaal`
- ✗ `raamwerk-neutraal` (calque van *framework-neutral*) → ✓ `stack-onafhankelijk`, `leverancier-onafhankelijk` + concrete uitleg
- ✗ `productie-naar-eval-trend` → herschrijf via Regel 3 (gewone-woorden-toets)

**Twijfeltest**: zou een Nederlandse productowner zonder IT-achtergrond dit woord in een vergadering gebruiken? Nee → vervang.

## Stap 3: Pre-write-scan op je voorgenomen tekst

**Voordat je Write of Edit aanroept** met BB/GR-content:

1. Render je geplande tekst mentaal (of in een scratch-buffer).
2. Scan op de vier hard rules:
   - Tel ` — ` in NL-tekst. Elke hit moet onderdeel zijn van een dubbele em-dash. Anders herschrijven.
   - Zoek `**.*?** —` en `**.*?**\s*—`. Vervang door `**...**: `.
   - Lees alle koppen. Bevatten ze `-architectuur`, `-engine`, `-tijdperk`, `-pijplijn` of vergelijkbare abstracties? Herschrijf naar gewone-woorden.
   - Grep `tegengift|handcureren|hand-cureren|kwartaal-cadans|raamwerk-neutraal` op het hele concept. Hits zijn calques (Regel 4) — vervang vóór Write.
3. Pas pas dán Write/Edit aan.

**Test op jezelf:** als je tijdens het schrijven van *deze* skill of *deze* sectie de regel hebt geschonden, ondermijnt dat de skill. Scan ook de tekst die jij zelf voor de skill produceert.

## Stap 4: Canoniek BB-pagina-skelet

```yaml
---
code: BB_0X
name: <Volledige naam>
tagline: "<Een zin van 6-10 woorden>"
icon: "<emoji>"
order: <1-7>
quote: "<Beste anker-citaat uit de bronnen>"
quoteAuthor: "<Naam (publicatie, jaar)>"
checklist:
  - "<Vraag 1?>"
  - "<Vraag 2?>"
  # 8-10 vragen totaal, vraagvorm, concreet, meetbaar
quickStart:
  - |
    Strategisch: <directie/leiderschap, eerste logische stap>.
    <Twee tot vier zinnen die de strategische beslissing verhelderen>
  - |
    Tactisch: <productowner/domain-owner, eerste logische stap>.
    <Twee tot vier zinnen>
  - |
    Operationeel: <architect/team, eerste logische stap>.
    <Twee tot vier zinnen>
auditExample:
  title: "AI-Readiness Audit"
  description: "<Authentiek voorbeeld uit Robin's praktijk; geen generiek scenario>"
evidence:
  - "<3-5 concrete bewijzen dat de BB goed draait>"
---

import BBDisclosure from '../../components/bb-detail/BBDisclosure.astro';

## Wat is <BB-naam>?

<2-3 alinea's kern-definitie + relatie tot nabijgelegen BB>

<BBDisclosure title="<Kop in gewone-woorden-toets>">
<Inhoud>
</BBDisclosure>

<!-- 6-7 BBDisclosures totaal, elk een volledige deelverhaalstructuur:
     - De evolutie / waarom dit nu belangrijk is
     - Het mechanisme / de empirische basis
     - De toolbox / hoe je het aanpakt
     - Een stille faalmodus / tegenkracht
     - Cross-bouwsteen of cross-guardrail-integratie
     - "In de praktijk" — pragmatische principes + koppelingen -->
```

**Drie-niveau Quick Start is verplicht.** Geen van de drie mag ontbreken. Elk niveau begint met een werkwoord en eindigt met een concrete actie. Labels (`Strategisch:`, `Tactisch:`, `Operationeel:`) staan expliciet in de tekst, niet alleen impliciet in de structuur.

## Stap 4b: Canoniek GR-pagina-skelet

GR-pagina's volgen een eigen vast skelet, parallel aan het BB-skelet maar met EU Trustworthy AI als kennisanker. De pilot is `frontend/src/content/guardrails/robustness.mdx`; gebruik die bij elke nieuwe GR als template-pagina.

```yaml
---
code: GR_0X
name: <Volledige naam>
euTerm: "<EU-term uit HLEG/AI Act, bv. 'Privacy and data governance'>"
tagline: "<Een zin van 6-10 woorden>"
icon: "<emoji>"
order: <1-7>
quote: "<Anker-citaat uit HLEG, ALTAI of EU AI Act>"
quoteAuthor: "<Naam (publicatie, jaar)>"
checklist:
  - "<Vraag 1?>"
  # 8-10 vragen, vraagvorm, concreet, meetbaar, gekoppeld aan het GR-kader
operationalFocus:
  - "<Concreet operationeel principe 1>"
  # 5-6 punten: pragmatische principes, geen checklist-vragen
quickStart:
  - |
    Strategisch: <directie/risicocomité, eerste logische stap>.
  - |
    Tactisch: <productowner/domain-owner, eerste logische stap>.
  - |
    Operationeel: voor laag-risico-systemen <baseline>. Voor hoog-risico-systemen <volwassen niveau>. <Slot-zin die voor beide geldt>.
legislation:
  - name: "EU AI Act Art. <X>"
    relevance: "<Hoe dit artikel deze GR raakt>"
  # 8-10 items: AI Act + ISO/IEC + NIST AI RMF + sector-specifiek (AVG, NIS2, etc.)
auditExample:
  title: "AI-Readiness Audit: <kernzin van de GR>"
  description: "<Authentiek voorbeeld uit Robin's praktijk>"
evidence:
  - "<3-5 concrete bewijzen dat de GR goed draait>"
---

import BBDisclosure from '../../components/bb-detail/BBDisclosure.astro';

## Wat is <GR-naam>?

<Pacing-opener (1-3 zinnen die de lezer ophalen bij herkenbare pijn): toezichthouder die vragen stelt, gebruiker die onverwacht antwoord krijgt, versie-wijziging die iets stilletjes anders maakt. Geen definitie eerst.>

<Definitie-alinea (2-3 zinnen): wat is deze GR, geen enkele eigenschap maar een verzameling.>

<Plaatsing in EU Trustworthy AI-traditie: HLEG (2019) → ALTAI (2020) vier sub-domeinen → EU AI Act (2024-2026) als wettelijke verankering. Glossary-links: /begrippen#hleg, /begrippen#altai, /begrippen#eu-ai-act.>

<Identiteits-zin: "Organisaties die hier scherp op sturen verschillen van organisaties die het niet doen op één punt: ...">

<BBDisclosure title="Het kader (GR-specifieke vier-of-meer domeinen)">
<ALTAI-domeinen of GR-eigen kader; per domein meetpunten en tegenmaatregelen.>
</BBDisclosure>

<BBDisclosure title="Wat de wet eist (en wat niet)">
<EU AI Act-artikelen, ISO/IEC-normen, sector-wetgeving (AVG, NIS2, etc.). Sluit altijd af met vertaal-alinea in vorm: "Voor de meeste organisaties komt deze stapel neer op X praktische dingen: ...">
</BBDisclosure>

<BBDisclosure title="<Aantal> valkuilen en hoe je ze ontwijkt">
<6 tot 8 anti-patronen met directe tegenmaatregel. Genummerd. Geen beschuldigend taalgebruik in de naam.>
</BBDisclosure>

<BBDisclosure title="In de praktijk: drie sectoren, drie gezichten">
<Vaste drietal: zorg + landelijke overheid + lokale overheid. Authentieke 2025-2026 cases met verifieerbare bron en concrete cijfers.>
</BBDisclosure>

<BBDisclosure title="Tooling die je in 2026 wilt hebben">
<Vier lagen of GR-eigen indeling. Concreet en met tooling-namen, alleen als geverifieerd.>
</BBDisclosure>

<BBDisclosure title="Het koppelpunt met andere bouwstenen en waarborgen">
<Welke BBs operationaliseren deze GR (3-4 stuks), welke andere GRs raken aan deze (2-3 stuks). Cross-refs altijd in eerste-vermelding-vorm: naam + code + kernzin.>
</BBDisclosure>
```

**GR-specifieke regels:**

- Cross-refs naar andere GRs in de koppelpunt-sectie volgen dezelfde "naam + code + kernzin"-regel als BBs. Voorbeeld: `Privacy (GR_03: dataminimalisatie, doelbinding, betrokkene-rechten) overlapt op ...`. Bij eerste vermelding geen kale `GR_03`.
- `frontend/src/lib/gr-bb-links.ts` is de inverse van `lib/bb-guardrail-links.ts`: hier vul je in welke BBs deze GR operationaliseren. Vergeet die data-update niet, anders rendert de "Bouwstenen die deze waarborg operationaliseren"-sectie leeg.
- De Operationele Quick Start heeft bij voorkeur een laag-risico-baseline én een hoog-risico-uitwerking; dit maakt de pagina relevant voor MKB-lezer in lichtere context én enterprise-lezer in zware context. (Aanleiding: `robustness.mdx` na /veranderkundige-pass, mei 2026.)
- Het EU-term-veld in de frontmatter wordt gerenderd in de hero onder de tagline. Gebruik exact de Engelse term uit HLEG/AI Act, niet een vertaling: dit is het ankerpunt voor lezers die naar de officiële documenten teruggaan.

## Stap 5: Schrijfstijl in de body

Onderstaande regels zijn condensaten van de gids §1-§16. Lees de gids voor uitwerking.

### Vakterm + uitleg of glossary-link

- Bij **eerste vermelding per BBDisclosure**: glossary-link `[term](/begrippen#slug)` plaatsen, niet "één keer per pagina". Lezers springen via inhoudsopgave of search willekeurig binnen op een uitvouw-blok. Per BBDisclosure moet de uitleg via klik bereikbaar zijn. Eindstand `model-engines.mdx`: 33 glossary-links, gemiddeld 3-4 per BBDisclosure.
- Glossary heeft tooltips: parenthese is dan duplicaat. Weglaten tenzij vloeiendheid lijdt (zie gids §15 voor de canonieke termen-tabel)
- Geen jargon-voor-jargon: `kennisgraaf` → `kennisnetwerk (entiteiten als knooppunten, relaties als verbindingen)`

### Business-NL-test ("grootouder-test")

Voor elke vakterm of formulering: zou iemand zonder IT-achtergrond dit begrijpen? Concrete voorbeelden uit `model-engines.mdx`-review die alsnog moesten worden vertaald:

- *anti-patroon* → "meest-gemaakte ontwerpfout"
- *enterprise-taken* → "zakelijke taken"
- *probabilistisch* → "waarschijnlijkheidsmatig (kans-gebaseerd, niet-deterministisch)"
- *ambigu* → "meerduidig"
- *bij schaal* → "bij voldoende volume"
- *native* → "rechtstreeks ondersteund" of "ingebouwd"
- *inferentiekosten* → "draaikosten (de kosten van elk antwoord dat het model produceert)"
- *HTTP 200-respons* → "technisch geslaagde aanvraag (server-status 'OK')"
- *upstream-incidenten* → "storingen bij de hoofd-aanbieder"

Als een term op de eerste lees-pass jargonachtig aanvoelt: of vervang door NL, of leg direct inline uit tussen haakjes.

### Geen code-style backticks of HTTP-statuscodes in business-tekst

- ✗ `` `fallback_activation_rate` `` → "stijgend percentage aanvragen dat naar het fallback-model wordt doorgeschakeld"
- ✗ "HTTP 429 rate-limit-fouten" → "rate-limit-fouten"
- ✗ "HTTP 200-respons" → "technisch geslaagde aanvraag"

Backticks horen bij code, niet bij business-NL. Code-style metric-namen zijn voor dashboards, niet voor doorlopende tekst.

### Eenzijdige claims toetsen

Bij elke harde claim afvragen: **wat is de tegenkant?** Wie is de andere partij in dit verhaal? Wat verzwijg ik onbewust?

- ✗ "60% rate-limit-fouten = autonome agents in feedbackloops slaan tegen aanbieders-limieten" (legt schuld eenzijdig bij klant)
- ✓ "Aanbieders schalen niet snel genoeg op om de explosief gegroeide vraag bij te benen, en autonome agents verergeren dit doordat ze in feedbackloops tegen de limieten op slaan" (beide kanten)

Bij elke "enige/eerste/grootste"-formulering: heb je de uitzonderingen daadwerkelijk uitgesloten? Bij `model-engines.mdx`: "enige open-weight challenger" miste Kimi K2.6, GLM-5.1 en MiniMax M2.7 uit Q1-2026.

### Toezichthouders en regulators bij naam noemen

Generieke labels als "sectorale waakhonden voor zorg en onderwijs" of "de Nederlandse toezichthouders" zijn voor de lezer onbruikbaar — ze willen weten *welke* instantie ze moeten gaan bedienen. Concretiseer altijd bij naam:

- **Privacy/persoonsgegevens**: Autoriteit Persoonsgegevens (AP)
- **Financiën**: Autoriteit Financiële Markten (AFM), De Nederlandsche Bank (DNB)
- **Markttoezicht/consument**: Autoriteit Consument en Markt (ACM)
- **Zorg**: Inspectie Gezondheidszorg en Jeugd (IGJ — kwaliteit en veiligheid, AI als medisch hulpmiddel), Nederlandse Zorgautoriteit (NZa — markttoezicht en bekostiging)
- **Onderwijs**: Inspectie van het Onderwijs

Voor de Nederlandse uitvoering van de EU AI Act (ontwerpwet april 2026) is per AI-toepassingsgebied nog niet limitatief vastgelegd welke toezichthouder is aangewezen. Vermeld die status expliciet ("liggen voor de hand", "vermoedelijk", "nog niet limitatief vastgelegd") in plaats van te suggereren dat de aanwijzing definitief is. Aanleiding: BB_05 Tool Integration noemde "sectorale waakhonden voor zorg en onderwijs" generiek; reviewer (Robin) wilde de concrete namen plus statusnuance.

### Business-termen NL

- Verkoop niet Sales; Productmanagement niet Product; Klantenservice niet Customer Success; Inkoop niet Procurement; Juridisch niet Legal
- Marketing mag (ingeburgerd)

### Concrete voorbeelden, geen code-voorbeelden

- ✓ "een klantdossier met vier verschillende adressen uit vier verschillende jaren"
- ✗ "test-fixtures in code-search"

### Cijfers met menselijke eenheid

- ✓ `32K tokens (ruim 20.000 woorden, omvang van een kort rapport)`
- ✗ `32K tokens` (alleen)

### Cross-refs: naam + code + kernzin bij eerste vermelding

- ✓ `Evaluation Loop (BB_07: meten, analyseren, verbeteren, opnieuw meten)`
- ✗ `BB_07`

### Gevolg-zinnen passief, niet anthropomorfisch

- ✗ "Een agent die de verkeerde definitie hanteert keurt korting goed..."
- ✓ "Een verkeerde definitie kan leiden tot kortingen die goed worden gekeurd op basis van niet-correcte criteria..."

### Tabellen vs. bullets

- Tabel alleen voor numerieke vergelijking, max 3 kolommen, korte cellen (<8-10 woorden)
- Inhoudelijke uitleg per categorie: bullets, ook als tabel "logisch" lijkt

## Stap 6: Post-write-validatie

Na schrijven en vóór doorgeven aan de gebruiker:

1. **Em-dash-scan**: `grep -c " — " <bestand>`. Hits inspecteren: elke hit moet onderdeel zijn van een dubbele em-dash óf in een Engels citaat staan.
2. **`**bold** —`-scan**: `grep -E '\*\*[^*]+\*\* —' <bestand>`. Mag geen hits geven.
3. **Astro check**: `cd frontend && npx astro check`. Moet 0 errors geven.
4. **Sectie-koppen-toets**: lees alleen de koppen. Bevatten ze `-architectuur`, `-engine`, `-tijdperk`, `-pijplijn`? Herschrijf.
5. **Drie-niveau Quick Start aanwezig?** Strategisch, Tactisch, Operationeel; allemaal als label in de tekst.
6. **Cross-refs eerste-vermelding-vorm?** Voor elke andere BB/GR die je noemt, eerste keer met naam + code + kernzin.
7. **Terminologie-consistentie-grep**: pak de term-tabel uit Stap 1b. Voor elke Engelse term die je hebt vertaald, grep op de Engelse vorm in de body (`grep -nE "\b<engelse-term>\b" <bestand>`). Hits moeten te verklaren zijn (canonieke parenthese, citaat, framework-eigennaam) of vervangen worden. Voorbeelden: `\bstream\b`, `\bvalue stream\b`, `\bplaybook\b`.
8. **Numerieke consistentie-check**: voor elke uitspraak in de frontmatter die een aantal noemt ("zeven dimensies", "vijf hefbomen", "drie spelers"), tel de overeenkomstige body-elementen handmatig. Bij `model-engines.mdx` bleken vier numerieke claims fout: vier→zeven dimensies, drie→vier spelers, vijf→zes hefbomen, "Hefboom 5: open-source migratie" → "open-weight migratie".
9. **Frontmatter↔body diff-scan**: vergelijk de exacte bewoordingen in `checklist`, `evidence`, `quickStart`, `auditExample` met de overeenkomstige body-koppen of bullet-titels. Voorbeeld-mismatch: "ecosysteem-volwassenheid" (frontmatter) vs "ecosysteem en integratie-gemak" (body H3-bullet).
10. **Sectie-bewust glossary-link-check**: voor elke begrippenlijst-term die op de pagina voorkomt: per BBDisclosure de eerste vermelding linken (niet "één keer per pagina"). Snelle check: `grep -c "begrippen#<slug>" <bestand>` moet ongeveer gelijk zijn aan het aantal BBDisclosures waarin de term voorkomt.
11. **Inhoudelijke-feiten-check** (kritisch bij externe frameworks en harde claims): voor elke claim over een extern framework, benchmark-score, prijs, releasedatum, of "enige/eerste/grootste"-uitspraak moet je de primaire bron hebben gezien. Geen plausibel-klinkende reconstructie uit context. Bij twijfel: WebFetch op de primaire URL of grep in lokale `docs/research/`-pakketten op `verified`-stempel. (Aanleiding: BB_02-concept noemde verzonnen unFIX-typen; BB_06-concept claimde "factor 1.250 prijsverschil" zonder onderbouwing en "enige open-weight challenger" terwijl Kimi/GLM/MiniMax bestonden.)
12. **Eenzijdige-claims-check**: voor elke causale uitspraak ("X gebeurt door Y"): is dit het complete plaatje, of is er een andere kant? Bij `model-engines.mdx`: "60% rate-limit-fouten = agents in feedbackloops" miste de leveranciers-capaciteit-kant.
13. **Code-style-jargon-scan**: `grep -nE "\\\`[a-z_]+\\\`" <bestand>`. Hits inspecteren: backticks horen bij code, niet bij business-NL. Vervang `` `metric_name` `` door een NL-omschrijving.
14. **KnowledgeItem-koppelingen reviewen**: open `backend/app/graph/seed.py` en grep op de huidige BB-naam. Klopt de lijst gekoppelde KnowledgeItems? Staan er bronnen tussen die thuishoren bij een andere BB? (Aanleiding: "Prompt Engineering for Generative AI" was foutief gekoppeld aan Model Engines i.p.v. alleen Prompt Design.)
15. **Re-seed + cleanup-protocol bij gewijzigde koppelingen**: als je een KnowledgeItem-aan-BB-relatie hebt versmald in `seed.py`, draai dan: (a) `python backend/scripts/seed_graph.py` voor toevoegingen, (b) een Cypher `DELETE`-query voor de stale relatie (`seed.py` is idempotent voor toevoegen, niet voor verwijderen), en (c) **astro dev-server herstarten**: `getStaticPaths` voert de Neo4j-fetch alleen op startup uit, dus de pagina toont oude data tot je `pkill -f "astro dev"` plus `npm run dev` doet. Verifieer met `curl http://localhost:8000/api/building-blocks/<BB-naam>/items` (API) én via een browser-refresh op `http://localhost:4321/framework/<slug>` (gerenderde pagina).
16. **Body↔guardrail-link-data-consistency**: open `frontend/src/lib/bb-guardrail-links.ts` en zoek de entry voor de huidige BB-slug. Klopt het aantal en de codes met wat de body in de "In de praktijk"-BBDisclosure claimt onder *"Het koppelpunt met andere bouwstenen en guardrails"* (telwoord + opsomming GR_0X)? De mapping wordt los van de body gerenderd in de "Gekoppelde guardrails"-sectie van de BB-detailpagina; een mismatch is voor de lezer een direct zichtbare inconsistentie. (Aanleiding: BB_05 Tool Integration body claimde "raakt vier guardrails direct" met GR_01/02/03/07, terwijl de mapping er drie had — GR_01 ontbrak.)
17. **Calque-scan**: `grep -nE "tegengift|handcureren|hand-cureren|kwartaal-cadans|raamwerk-neutraal" <bestand>`. Mag geen hits geven. Voor risico-samenstellingen die een nieuwe calque kunnen verbergen: `grep -nE "[a-z]+-cadans|[a-z]+-pijplijn|[a-z]+-engine|[a-z]+-tijdperk" <bestand>` en inspecteer per hit. Volledige groei-lijst: `schrijfstijl-bb.md` §1b. (Aanleiding: BB_07 Evaluation Loop, "tegengift" 8× in één blok, plus 4 andere calques die spell- en stijlcheck passeerden.)
18. **Kennisbank-curatie-meegroei** (verplichte laatste stap vóór "klaar"): open `backend/app/graph/seed.py` en filter op de huidige BB-naam. Bepaal de top 3 die de gebruiker straks ziet — sortering: `curation_score` DESC, dan title alfabetisch. Lees de samenvatting (`summary_nl`) van die 3 en stel jezelf de vraag: *gaan deze items echt over deze BB, of zijn ze tangentieel meegekomen omdat een tag conceptueel raakte?* Bij tangentieel: ofwel `building_blocks`-lijst van het off-topic item versmallen (BB-tag verwijderen), ofwel `curation_score` van een meer-relevant item ophogen zodat het in de top 3 komt. Daarna re-seed en verifieer. (Aanleiding: BB_07 Evaluation Loop top 3 was Budzyń-deskilling/Kahneman-intuition/Dell'Acqua-frontier — alle drie eigenlijk over BB_01 Knowledge.)

Als één van deze checks faalt: terug naar Stap 3 (pre-write-scan) op het probleemgedeelte.

## Gotchas

- **Je eigen voorstellen in deze sessie**: scans gelden ook voor zinnen die je in chat aanbiedt aan de gebruiker, niet alleen voor file-content. Een voorstel met een losse em-dash ondermijnt de skill-regel.
- **Engels-naar-Nederlands-vertaling**: anglicismen sluipen via idiomen ("aan het einde van de dag" uit *at the end of the day*; "alles-en-de-keukenkraan" uit *everything and the kitchen sink*). Test: zoek de uitdrukking in Van Dale of een NL-nieuwsbron — geen hits = anglicisme.
- **Frontmatter consistentie**: bewoording in `checklist`, `quickStart`, `evidence`, `auditExample` moet dezelfde termen gebruiken als de body. Als de body "ecosysteem en integratie-gemak" zegt, niet in checklist "ecosysteem-volwassenheid". Bij genummerde claims ("zeven dimensies") tellen of het overeenkomt met de body.
- **Re-seed verwijdert geen oude relaties**: `seed.py` is idempotent voor toevoegen via `MERGE`, niet voor verwijderen. Wanneer je een KnowledgeItem-aan-BB-koppeling versmalt door uit `building_blocks`-lijst te halen, blijft de oude `:RELATES_TO`-relatie staan in Neo4j tot je hem expliciet via Cypher `DELETE`'t. Zonder cleanup is de wijziging onzichtbaar in productie.
- **`schrijfstijl-bb.md`-log bijwerken**: na elke afgeronde BB/GR voeg je een entry toe aan §"Log: welke pagina's zijn hiermee geschreven/herschreven" met datum, pagina, status en eventueel nieuwe regels die uit de review naar voren kwamen.

## Case-study: lessen uit `model-engines.mdx` (april 2026)

Bij de review van BB_06 zijn ~50 termen alsnog uitgelegd of vervangen, een derde van de harde claims bleek achterhaald, eenzijdig of fout, vier numerieke inconsistenties tussen frontmatter en body geconstateerd, en een foutieve KnowledgeItem-koppeling (Prompt Engineering O'Reilly aan Model Engines) gevonden. Concrete patronen die deze skill nu probeert af te dwingen:

- **Drift in vakjargon**: HTTP-statuscodes, code-style backticks, en "tier-strategie met caching"-soort handen kortingen die op zichzelf onverstaanbaar zijn voor business-NL-publiek.
- **Drift in onderbouwing**: "factor 1.250 prijsverschil" tussen niet-vergelijkbare modellen, "enige open-weight challenger" zonder dat Kimi/GLM/MiniMax waren uitgesloten, "break-even bij €X cloudkosten" als statisch getal in plaats van als terugverdientijd.
- **Drift in volledigheid**: vier wereld-modellen genoemd terwijl er vijf waren (Marble vergeten), Cosmos 3 (GTC maart 2026) niet meegenomen, Tesla niet als grensgeval benoemd.
- **Drift in nuance**: Datadog-rapportage uitgelegd als "agents in feedbackloops slaan tegen aanbieders-limieten" zonder de leveranciers-capaciteit-kant te benoemen.

Voor de volgende BB: **investeer aan de voorkant** (Stappen 1b/1c/1d) zodat dit soort drift wordt voorkomen, in plaats van pas tijdens woord-voor-woord-review door Robin gerepareerd.

## Referenties

| Wanneer | Lees |
|---------|------|
| Volledige stijlgids (verplicht bij eerste BB/GR-sessie) | `~/ODIN/projecten/BeeHaive/.claude/schrijfstijl-bb.md` |
| BB-template-voorbeeld (volledig) | `frontend/src/content/building-blocks/knowledge.mdx` |
| BB-template-voorbeeld (baseline) | `frontend/src/content/building-blocks/dynamic-context.mdx` |
| GR-template-voorbeeld (pilot) | `frontend/src/content/guardrails/robustness.mdx` |
| Glossary-slugs voor links | `frontend/src/data/begrippen.ts` |
| KnowledgeItems per BB | `backend/app/graph/seed.py` |
| GR-aan-BB-koppelingen | `frontend/src/lib/gr-bb-links.ts` |
| BB-aan-GR-koppelingen | `frontend/src/lib/bb-guardrail-links.ts` |
