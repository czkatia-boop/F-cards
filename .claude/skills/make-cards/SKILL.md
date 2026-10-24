---
name: make-cards
description: Turn a textbook photo, word list or topic into ready-to-paste cards and exercises for the Spellbook apps (harry.html / hermione.html). Use when the user sends a photo of a textbook page, a vocabulary list or a grammar table, or asks for cards, conjugation tables, gap-fill sentences or a unit test for Harry or Hermione.
---

# make-cards: textbook page → text to paste into Spellbook

The output of this skill is **plain text the user pastes into the app**, never code changes. Do not edit `build/template.html` for this.

## Who is who

- **Harry** (`harry.html`) is the older child: **English and German**.
- **Hermione** (`hermione.html`) is the younger child: **English only**. Never produce German material for Hermione.
- The app is in Polish and every translation (the back of a card) is **Polish**, unless the user says otherwise.
- The user writes to you in Russian. Answer in Russian, but the card text itself is the target language + Polish.

## Structure in the app

`Unit` (about 8 a year, has one language) → `topic` (called *zestaw*; a small theme) → cards.
The unit's "Sprawdzian" tests every card of every topic in it, typed, so keep a topic's words in one unit.

Before writing cards, find out (ask in one short question if the photo does not make it obvious):
1. Which child / app.
2. Language and unit name (e.g. "Unit 3"). Units are created in the app: Dodaj → *Nowy unit* (name + language).
3. Topic name (e.g. "Tiere"). Created in Dodaj → *Nowy zestaw* (pick the unit), or choose "+ Nowy zestaw…" inside the batch forms and pick the unit there.

## The three formats (all go in Dodaj; open it with the gear icon, top right of the home page)

Check your output against these rules, they mirror the app's parser.

### 1. Words and phrases: section "Wiele kart naraz"

One card per line: `foreign word — Polish translation — example (optional)`

```
der Hund — pies — Der Hund schläft. — Pies śpi.
die Katze — kot
to brew — warzyć — He brews tea. — Parzy herbatę.
```

- Separators: ` — ` (spaces around the dash), ` – `, ` - `, a tab, or `;`. The example may itself be two parts joined by ` — ` (sentence — its translation).
- **Do not** use `;` or a spaced hyphen ` - ` inside a word, translation or example, it would split the line. Use a comma instead.
- No pronunciation here (IPA only exists in the single-card form). Skip it.
- **German nouns always with the article and capitalised**: `der Bahnhof`, not `Bahnhof`. The app checks German strictly: exact case, umlauts (ä ö ü ß) and article.
- English verbs as `to go`. Plain words in lowercase unless they are proper nouns.
- Only **single words** (optionally with `der/die/das/to/the/a/an`) are typed in write mode and in unit tests. Multi-word phrases and idioms are flipped and self-graded, which is fine; do not shorten a phrase just to make it typeable.
- One meaning per card. If a word has several translations, give the one the textbook uses, or separate cards.

### 2. Conjugation tables: section "Ćwiczenia: odmiana i luki"

`infinitive | tense | forms separated by commas | translation (optional)`

```
gehen | Präsens | gehe, gehst, geht, gehen, geht, gehen | iść
fahren | Präsens | fahre, fährst, fährt, fahren, fahrt, fahren | jechać
gehen | Perfekt | bin gegangen, bist gegangen, ist gegangen, sind gegangen, seid gegangen, sind gegangen | iść
to go | Present | go, go, goes, go, go, go | iść
```

- Exactly **six forms** in the order 1sg, 2sg, 3sg, 1pl, 2pl, 3pl, matching the pronoun set chosen in the app's "Zaimki do odmiany" select (Niemiecki: ich, du, er/sie/es, wir, ihr, sie/Sie; Angielski: I, you, he/she/it, we, you, they; also Polish, French, Spanish, Italian).
- Another number of forms or your own labels: write `label=form` for every item, and set the select to "Własne (zaimek=forma)": `ich=gehe, du=gehst`. Use this for imperatives, modal verbs with only some persons, etc.
- No commas inside a form. A form may offer alternatives with `/`: `gehe/geh` accepts either.
- German forms are checked strictly (case, umlauts).

### 3. Gap-fill sentences: same section "Ćwiczenia: odmiana i luki"

`sentence with ___ | answer | Polish translation (optional) — grammar note (optional)`

```
Ich sehe ___ Hund. | den | Widzę psa. — biernik
Ich bleibe zu Hause, ___ ich krank bin. | weil | Zostaję w domu, bo jestem chory. — szyk końcowy
Ich gehe ___ ___ Schule. | in; die | Idę do szkoły. — biernik po in
She ___ to school every day. | goes | Ona chodzi do szkoły codziennie.
```

- The gap is exactly three underscores `___`. Several gaps: answers separated by `;`, in the order of the gaps.
- The translation is shown while the child answers; the text after ` — ` (a note) is shown only after checking.
- One clear answer per gap. Prefer gaps for grammar the textbook page is teaching (case, preposition, verb form, word order) and put the needed hint in brackets if the answer is otherwise ambiguous, e.g. `Ich sehe ___ Hund. (der Hund)`.
- No `|` inside the sentence.

## Delivering the cards: content pack (default) or paste blocks

**Default: a content pack.** One chapter = one file `content/<child>/<chapter-id>.txt` (child = `harry` or `hermione`). `build/build.py` embeds it into that child's app, which imports it once and automatically the next time it is opened. Nothing has to be pasted on the phone. Commit it on a branch, run the build (see below), open a PR; after it is merged the child gets the unit.

File format (the lines inside a section are exactly the lines of formats 1-3 above):

```
@unit Kapitel 1 — Hallo! Wie geht's?
@lang Niemiecki

@topic Begrüßung und Abschied
@words
Guten Morgen — Dzień dobry (rano)

@topic Verben im Präsens
@rituals
gehen | Präsens | gehe, gehst, geht, gehen, geht, gehen | iść
Ich ___ Lena. (heißen) | heiße | Nazywam się Lena.
```

- `@words` sections use format 1; `@rituals` sections use formats 2 and 3 (a topic may mix conjugation and gap-fill lines). Lines starting with `#` are comments.
- **List topics in the order they should be learned**: the home button "Zacznij naukę" walks through the topics in file order (the first topic is treated as the newest).
- **Pack id = file name.** Never rename a published pack, the app would import it a second time. For corrections after publishing, edit the file only if nobody has used it yet; otherwise add a new pack or tell the user to fix the card in Dodaj/Karty.
- An existing unit with the same `@unit` name (made by hand) makes the app skip the import, so a pack never duplicates hand-made cards.
- `@lang` must be a language the child studies (Hermione: Angielski only).

Build and check before committing (from the repo root; the third argument is any file that contains the tear-edge `clip-path` polygons, e.g. the current `harry.html`):

```
cp harry.html /tmp/design.html && python3 build/build.py . /tmp/design.html
```

The build fails with an assertion if a topic is empty or `@unit`/`@lang` are missing. Then open `harry.html` in a browser and check: the unit appears once, topic card counts match your announcement, and a Sprawdzian over the unit with all answers correct scores 100%.

**Alternative: paste blocks.** If the user wants to type the material in themselves, or it is a few cards, give blocks for the Dodaj forms as described in the workflow below.

## Workflow for a photo

1. **Read the page carefully.** Transcribe vocabulary exactly as printed. If something is unreadable or you are unsure, say so and ask; never guess a word silently.
2. **Sort the content**: vocabulary list → format 1; verb tables → format 2; grammar exercises or example sentences with a rule → format 3.
3. **Stay on the page.** Use the words and verbs the textbook gives. When you add something the page does not contain (an article, a plural, a missing form, an extra example), mark it as "dopisane" in your note so the user can check it.
4. **Make your own sentences**; keep entries short (words, forms, short sentences). Do not transcribe whole textbook exercises.
5. **Level**: match the child. Hermione is younger, so simple sentences and basic words.
6. **Output**, in Russian: first show the user the unit and topic names with card counts per topic, and a short note: what you added yourself ("dopisane"), what was unclear. Then either create the pack file and branch (default), or give each format as a separate code block with one line above it saying where to paste it (Dodaj → which section, which *Zestaw*/*Unit* to select, which *Zaimki* if conjugation). Open a PR only when the user asks.
7. **Reminders worth one line**: when pasting by hand, add a topic in one sitting (the home button "Zacznij naukę" trains everything still due that was added within an hour of the last addition, then moves on to older additions); after a big hand import make a backup (Ustawienia → Zapisz kopię).

## Self-check before sending

- Counts: lines in the block = cards you announce.
- Format 1: no stray `;` or ` - ` inside a field; German nouns have article and capital letter.
- Format 2: six comma-separated forms (or `label=form` for every item); no `|` or comma inside a form.
- Format 3: contains `___`, number of answers = number of gaps, answers separated by `;`.
- Nothing German for Hermione.
- Quick test if a browser is available: open the page, run `parseBatch(text)` or `parseRitual(text, 'Niemiecki')` in the console, and expect no `null` entries.
