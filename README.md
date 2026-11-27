# Distracted by Christ

A single scrolling page to keep open in a browser tab instead of a social feed: a short prayer
when you open the tab, gospel homilies from the Church Fathers, saint quotes, pray-along chaplets,
the Liturgy of the Hours, a litany for the day, "in a year" series and an endless feed.
Your browser remembers your place in all of it.

## Files

| File | What it is |
|---|---|
| `yesterday.md`, `today.md`, `tomorrow.md` | The day's texts for three UTC dates (T−1, T, T+1). Rolled forward every day at 00:10 UTC. The page shows the one dated for the reader's local date. |
| `library.md` | Fixed texts: prayers, chaplets, rosary mysteries, aspirations, "in a year" series. |
| `src/template.html` | The page itself (HTML, CSS, JS). Edit this, never `index.html`. |
| `build.py` | Inlines `library.md` and the three day files into `index.html`. |
| `index.html` | Built output. Committed so it can be opened or hosted as-is. |

## Use

```bash
python3 build.py        # after any edit to a day file, library.md or the template
xdg-open index.html     # or open it in any browser; works from disk
```

When served over http(s) (S3, GitHub Pages, `python3 -m http.server`) the page fetches the day
files and `library.md` live and uses them instead of its inlined copies, so a host can update
the day files on their own. Opened from disk it uses the inlined copies.

## Daily update

Every date is a UTC calendar date. A scheduled Claude task runs daily at **00:10 UTC** and rolls
the buffer forward: `today.md` becomes `yesterday.md`, `tomorrow.md` becomes `today.md`, and a new
`tomorrow.md` is written for the UTC date 24 hours ahead. Before and after the shuffle it checks the
dates, so a missed or doubled run heals itself instead of corrupting the buffer. `CLAUDE.md` holds
the procedure.

Why three files cover everyone: local time runs from UTC−12 to UTC+14, so a reader's local date is
always within a day of the UTC date. Between runs the buffer holds T−1, T and T+1. In the ten
minutes before a run (T−2, T−1, T) every reader's date is still T−1 or T, except UTC+13/+14, whose
date is T, which is present. Readers stay covered through the run and the Pages deploy, as long as
the run lands within about ten hours.

Scheduled task (cloud `/schedule`):

- Cron: `10 0 * * *` (UTC)
- Prompt:

  ```
  In the distracted-by-christ repo, update it for the day: follow the daily rotation in CLAUDE.md
  ("Update it for the day"). Use UTC dates only (date -u +%F). Check the three day files' dates
  before and after the shuffle and self-heal rather than shuffling blindly; if every slot already
  holds the right date, do nothing. Rebuild with python3 build.py, commit the changed day files
  and index.html by name as "Update for <tomorrow.md's date>", and push to main.
  ```

You can also ask Claude to "update it for the day" by hand. A shorter prompt for writing a single
day file is on the page itself under *Prompt for the daily refresh*.

## Hosting

Served by GitHub Pages from `main` (repo root): https://gititgoro.github.io/distracted-by-christ/
Every push redeploys. `.nojekyll` stops Pages turning the markdown files into HTML, so the page
can fetch them as-is.
