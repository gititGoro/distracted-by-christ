# CLAUDE.md

Static devotional page. No dependencies, no framework. See README.md for the file layout.

## "Update it for the day"

0. **"Today" is the date in South Africa (Africa/Johannesburg, UTC+2)**, not the machine's clock.
   Get it with `TZ=Africa/Johannesburg date +%F`. The scheduled run fires at 02:10 UTC (04:10 there),
   so both agree, but always use the South African date in case the schedule moves.
1. Work out that day's liturgical day for the Roman Rite (General Roman Calendar): weekday name,
   feast or memorial, season, liturgical colour, psalter week (week of Ordinary Time mod 4;
   Advent/Lent/Easter weeks start at week I), and the Mass readings.
2. Rewrite `day.md` in the exact format of the current file:
   - Front matter: `date` (YYYY-MM-DD, the South African date from step 0), `day`, `memorial` (blank if none), `season`,
     `colour` (green | violet | white | red | rose | black), `psalter`.
   - `# Aspirations`: 2 to 4 that suit the day or feast. Generic ones live in `library.md`.
   - `# Homilies`: 5 or 6. The day's Gospel first, then the coming Sunday's, then passages that
     fit the season. Each: `## Reference | label`, the passage as `> ` lines, then
     `### Father | Work, section` and two short paragraphs. Prefer the Office of Readings.
   - `# Litany | Name`: the whole litany as `- invocation | response` lines (a line without `|`
     repeats the last response), then the closing prayer. Choose by feast; otherwise by weekday:
     Sunday Holy Name, Monday Holy Spirit, Tuesday Holy Angels or Precious Blood, Wednesday
     St Joseph, Thursday Blessed Sacrament, Friday Sacred Heart, Saturday Loreto. Give the
     reason on a `! ` line.
   - `# Saints`: 6 to 8 quotations, `## Saint | Work, section`, around the day's saint, feast or Gospel.
   - `# Hours`: `## Lauds`, `## Terce`, `## Sext`, `## None`, `## Vespers`, `## Compline`, each
     split into `### Step | note` parts following the psalter week. Antiphons and instructions
     go on `! ` lines. Use a public-domain or freely usable translation (RSV/Douay style).
3. `python3 build.py`, then commit `day.md` and `index.html` as `Update for YYYY-MM-DD` and push.

## Rules

- **Never invent a quotation.** Quote real text with an exact source. A paraphrase is marked
  `(adapted)`. If unsure of a passage, choose one you are sure of.
- Edit `src/template.html`, never `index.html` directly; always rebuild.
- If the layout or format has changed, follow the current `day.md` and `src/template.html`
  rather than this file, and update this file to match.
- `library.md` changes only when asked (new chaplet, new series, playlist URLs).
- Stage files by name; never `git add -A`.
