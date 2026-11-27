# CLAUDE.md

Static devotional page. No dependencies, no framework. See README.md for the file layout.

## The three-day buffer

The site keeps three day files, `yesterday.md`, `today.md` and `tomorrow.md`. Each holds the texts
for one absolute calendar date, named by the `date:` in its front matter. **Every date is a UTC
calendar date.** The page picks whichever file is dated for the reader's own local date, so a
reader in any timezone (UTC−12 to UTC+14 is always within ±1 day of UTC) sees their own day
without the server knowing where they are. If none matches, it shows the nearest one with a
"texts are for <date>" banner.

The scheduled run fires daily at **00:10 UTC** (cron `10 0 * * *`, UTC).

### Date rule (the single source of truth)

A run at UTC instant `t` produces this target state, nothing else:

```
T = date -u +%F                       # UTC date of the run. Never TZ=..., never plain `date`.
yesterday.md   date: T-1              # date -u -d "$T -1 day" +%F
today.md       date: T
tomorrow.md    date: T+1              # the UTC date of t + 24h
```

## "Update it for the day" (the daily rotation)

0. Get `T` with `date -u +%F`, and the three target dates T−1, T, T+1. Read the `date:` of each
   existing day file.
1. **Normal run** (the previous run landed on T−1, so the files hold T−2, T−1, T):
   - Pre-shuffle check: `tomorrow.md`'s `date` must equal T. If it does not, do not shuffle; go to
     *Self-heal* below.
   - `today.md` → `yesterday.md`, then `tomorrow.md` → `today.md` (`git mv`, or copy and overwrite).
   - Write a new `tomorrow.md` for T+1 (see *Writing one day file*).
   - Post-shuffle check: the three `date:` values are exactly T−1, T, T+1.
2. **Self-heal** (a missed run, a double run, a late merge, or a bootstrap): for each slot
   (yesterday = T−1, today = T, tomorrow = T+1), if any existing file already holds that slot's
   date, move it into that slot; otherwise write that slot fresh. A file whose date is not one of
   the three is discarded. Fresh slots are written as in *Writing one day file*. **Never shuffle blindly**: a second blind shuffle on the same day would
   put T+1's texts in `today.md` and lose yesterday. A second run on the same UTC day finds every
   slot correct and is a **no-op**: it writes and commits nothing.
3. **Bootstrap** (no day files yet, or all stale) is just self-heal with nothing to reuse: write
   all three for T−1, T, T+1.
4. `python3 build.py`, then stage the day files you changed and `index.html` by name and commit as
   `Update for YYYY-MM-DD`, where the date is the new `tomorrow.md`'s date (T+1). Push. A no-op run
   commits nothing.

## Writing one day file (for date X)

1. Work out that date's liturgical day for the Roman Rite (General Roman Calendar): weekday name,
   feast or memorial, season, liturgical colour, psalter week (week of Ordinary Time mod 4;
   Advent/Lent/Easter weeks start at week I), and the Mass readings.
2. Write the day file in the exact format of the current ones:
   - Front matter: `date` (YYYY-MM-DD, the UTC date the file is for), `day`, `memorial` (blank if none), `season`,
     `colour` (green | violet | white | red | rose | black), `psalter`.
   - `# Aspirations`: 2 to 4 that suit the day or feast. Generic ones live in `library.md`.
     A line of Scripture is quoted word for word, with its reference: never change the speaker's
     person ("my words" stays "my words"). To pray a verse back to God, say so plainly
     ("Lord, your words will not pass away") or choose another aspiration.
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

## Rules

- **Never invent a quotation.** Quote real text with an exact source. A paraphrase is marked
  `(adapted)`. If unsure of a passage, choose one you are sure of.
- Edit `src/template.html`, never `index.html` directly; always rebuild.
- If the layout or format has changed, follow the current day files and `src/template.html`
  rather than this file, and update this file to match.
- `library.md` changes only when asked (new chaplet, new series, playlist URLs).
- Stage files by name; never `git add -A`.
