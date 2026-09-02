# MARKA London — Capsule Edition

Landing site for MARKA London, the first international edition of the MARKA
conference, held at the Design Museum in London on 13 October 2026 in partnership
with STEPEVI.

No build step, no dependencies — plain HTML, one stylesheet, and images.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | About MARKA London |
| `stepevi.html` | MARKA x STEPEVI |
| `speakers.html` | Speakers |
| `venue.html` | The Venue |

The home page runs: hero banner, a sticky ticker that pins below the header on
scroll, a four-box programme grid, the Event Day schedule, How to Attend, Journal,
and the footer. The four inner pages share one layout — title, banner figure, body
copy — and link from both the programme boxes and the footer.

## Running it

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

Opening `index.html` directly works too, but serving it is closer to production.

## Structure

- **Styles** — `styles.css` holds the shared palette, type and components. Each
  inner page also carries its own `<style>` block for the L2 layout rules. Those
  blocks are currently duplicated across the four pages; consolidating them into
  `styles.css` is the obvious next cleanup.
- **Palette** — defined as custom properties on `:root`. Ground `#2D302C`, accent
  `#640402`. Single theme; there is no light/dark switching.
- **Fonts** — Archivo (display) and Newsreader (body) from Google Fonts, both with
  real fallback stacks so layout holds if the fonts fail.
- **Images** — the programme boxes swap on hover: `<name>-bw.jpg` shows at rest and
  cross-fades to `<name>.jpg`. Keep that naming when adding tiles. Assets are
  pre-sized for their slot rather than shipped at source resolution; banner images
  are pre-cropped to 21/9 so no hidden pixels are downloaded.
- **Motion** — the ticker and hover transitions are disabled under
  `prefers-reduced-motion`.

## Publishing to a Claude artifact

`index.html` and the inner pages are the source of truth. Artifacts supply their own
document skeleton and cannot load a local stylesheet, so the published copies are
generated:

```sh
python3 build-artifact.py   # writes dist/ (git-ignored)
```

`ARTIFACT_URLS` in that script rewrites the links between pages; entries are blank
until a page has been published. This flow is only needed for artifact previews — a
normally hosted site serves these files directly and does not need it.

## Content

Copy, images and the schedule are supplied by MARKA. The Design Museum Instagram
handle on the venue page should be verified before launch.
