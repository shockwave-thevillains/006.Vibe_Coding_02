# The Machine That Learned

A static website telling the history of artificial intelligence, from Alan Turing's 1936
universal machine to the transformer era &mdash; written in plain English for readers who are
not researchers.

**Palette:** white base, red `#FF0000`, black.
**Stack:** hand-written HTML/CSS/JS. No frameworks, no build dependencies, no trackers.

---

## Routes

Every section is a real path with its own document, not an anchor on one long page.

| Path | Page |
| --- | --- |
| `/` | Redirects to `/home/` |
| `/home/` | Overview, the boom-and-bust curve, chapter index |
| `/origins/` | 1936&ndash;1956 &middot; Turing, McCulloch&ndash;Pitts, Shannon, Dartmouth |
| `/goldenage/` | 1956&ndash;1973 &middot; Logic Theorist, the perceptron, ELIZA, SHRDLU |
| `/winters/` | 1973&ndash;1993 &middot; Lighthill, expert systems, two funding collapses |
| `/learning/` | 1986&ndash;2011 &middot; backpropagation, SVMs, Deep Blue, ImageNet |
| `/deep/` | 2012&ndash;2017 &middot; AlexNet, CNNs, GANs, AlphaGo |
| `/modern/` | 2017&ndash;now &middot; transformers, scaling laws, RLHF, agents |
| `/timeline/` | 53 milestones, filterable by era |
| `/people/` | Twelve profiles &mdash; builders and critics |
| `/glossary/` | 62 terms with live search |
| `/ethics/` | Bias, hidden labour, copyright, energy, automated decisions |
| `/risk/` | Misuse, alignment, the x-risk debate, regulation |
| `/future/` | AGI definitions, scaling limits, eight open questions |

The navbar links to all thirteen and marks the current page with `aria-current`. Below 1200px it
collapses into a toggle menu.

## Repository layout

```
build.py            generator: wraps each fragment in the shared shell
src/pages/*.html    page bodies (content only, no <head>, no navbar)
assets/css/style.css
assets/js/main.js   mobile nav, reading progress, timeline filter, glossary search
<slug>/index.html   generated output -- do not edit by hand
index.html          generated redirect to /home/
```

The shell (head, navbar, page header, pager, footer) lives in `build.py`. Adding a page means
adding one row to `PAGES` and one fragment in `src/pages/`; the navbar, footer columns and
previous/next links update themselves.

## Working on it

```bash
python3 build.py          # regenerate every <slug>/index.html
python3 -m http.server 8000
# then open http://localhost:8000/
```

Serve over HTTP rather than opening files directly &mdash; the clean directory URLs
(`../risk/`) need a server that resolves `index.html`.

Editing a generated `<slug>/index.html` directly will be overwritten on the next build. Edit
`src/pages/<slug>.html` instead.

## Illustrations

Every diagram is hand-written inline SVG in the page fragment that uses it: the boom-and-bust
curve, the Turing machine, the imitation game, the XOR separability proof, gradient descent,
the ImageNet error chart, the CNN feature hierarchy, attention weights, the training pipeline,
the predictive-policing feedback loop, the prompt-injection path, the EU AI Act risk pyramid,
and twelve emblems on the people page. No external images, no CDN, no licensing questions, and
nothing that can break offline. Each carries `<title>` and `<desc>` for screen readers.

## Accessibility and browser support

Skip link, landmark elements, `aria-current` on the active nav item, labelled form controls,
`prefers-reduced-motion` honoured, and body copy in black on white rather than red (pure red on
white is only used for large text, borders and accents, where the contrast ratio is adequate).
No build step, no polyfills; the JavaScript is optional &mdash; every page reads fine without it,
losing only the filter, the search and the mobile menu toggle.

## Deploying

It is a directory of static files. Any host works. For GitHub Pages, publish from this branch
and the routes work as written; `.nojekyll` is committed so the directories are served.
