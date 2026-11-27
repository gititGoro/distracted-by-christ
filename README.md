# Distracted by Christ

A single scrolling page to keep open in a browser tab instead of a social feed: a short prayer
when you open the tab, gospel homilies from the Church Fathers, saint quotes, pray-along chaplets,
the Liturgy of the Hours, a litany for the day, "in a year" series and an endless feed.
Your browser remembers your place in all of it.

## Files

| File | What it is |
|---|---|
| `day.md` | The day's texts. Rewritten every day. |
| `library.md` | Fixed texts: prayers, chaplets, rosary mysteries, aspirations, "in a year" series. |
| `src/template.html` | The page itself (HTML, CSS, JS). Edit this, never `index.html`. |
| `build.py` | Inlines both markdown files into `index.html`. |
| `index.html` | Built output. Committed so it can be opened or hosted as-is. |

## Use

```bash
python3 build.py        # after any edit to day.md, library.md or the template
xdg-open index.html     # or open it in any browser; works from disk
```

When served over http(s) (S3, GitHub Pages, `python3 -m http.server`) the page fetches `day.md`
and `library.md` live and uses them instead of its inlined copies, so a host can update
`day.md` on its own. Opened from disk it uses the inlined copies.

## Daily update

Ask Claude to "update it for the day" in this repo; `CLAUDE.md` holds the procedure.
The same instructions are on the page itself under *Prompt for the daily refresh*.
