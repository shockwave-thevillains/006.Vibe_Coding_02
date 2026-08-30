#!/usr/bin/env python3
"""Static site generator for "A History of Artificial Intelligence".

Each entry in PAGES becomes its own directory with an index.html, so the site
is served at real paths -- /home/, /origins/, /risk/ -- rather than anchors on
a single document. Page bodies live as HTML fragments in src/pages/<slug>.html
and are wrapped in the shared shell (header, navbar, pager, footer) below.

Usage:  python3 build.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES_DIR = ROOT / "src" / "pages"

SITE_NAME = "The Machine That Learned"
SITE_TAGLINE = "A history of artificial intelligence, from Alan Turing to today."

# slug, nav label, <title>, kicker, year range, meta description
PAGES = [
    ("home",     "Home",      "A History of Artificial Intelligence",
     "Start here", "1936 &ndash; today",
     "A complete, plain-English history of artificial intelligence: the people, the breakthroughs, the failures and the open questions."),
    ("origins",  "Origins",   "Origins of a Thinking Machine",
     "Chapter 01", "1936 &ndash; 1956",
     "How Alan Turing, Claude Shannon, McCulloch and Pitts, and the 1956 Dartmouth workshop turned 'can a machine think?' into a research field."),
    ("goldenage", "Golden Age", "The Golden Age and Its Limits",
     "Chapter 02", "1956 &ndash; 1973",
     "Logic Theorist, the perceptron, ELIZA, SHRDLU and Shakey: the first wave of AI, and the hard walls it ran into."),
    ("winters",  "AI Winters", "The AI Winters",
     "Chapter 03", "1973 &ndash; 1993",
     "The Lighthill report, the collapse of the expert-systems industry and Japan's Fifth Generation project: what happens when the money stops."),
    ("learning", "Learning",  "The Statistical Turn",
     "Chapter 04", "1986 &ndash; 2011",
     "Backpropagation, decision trees, support vector machines, Bayesian methods, Deep Blue and Watson: AI learns from data instead of rules."),
    ("deep",     "Deep",      "The Deep Learning Revolution",
     "Chapter 05", "2012 &ndash; 2017",
     "AlexNet, GPUs, convolutional networks, LSTMs, GANs and AlphaGo: the five years that made neural networks the default."),
    ("modern",   "Modern",    "Transformers, Scale and Generative AI",
     "Chapter 06", "2017 &ndash; today",
     "Attention, BERT and GPT, scaling laws, RLHF, ChatGPT, multimodal models and agents: how modern AI actually works."),
    ("timeline", "Timeline",  "The Full Timeline",
     "Reference", "1936 &ndash; today",
     "Every major moment in the history of artificial intelligence on one filterable timeline."),
    ("people",   "People",    "The People Behind the Machines",
     "Reference", "Twelve lives",
     "Turing, McCarthy, Minsky, Rosenblatt, Weizenbaum, Pearl, Hinton, LeCun, Bengio, Li, Hassabis and Gebru: who built the field, and who argued with them."),
    ("glossary", "Glossary",  "Glossary",
     "Reference", "62 terms",
     "Plain-English definitions of the vocabulary of artificial intelligence, from &lsquo;algorithm&rsquo; to &lsquo;zero-shot&rsquo;."),
    ("ethics",   "Ethics",    "Ethics: Fairness, Work and Ownership",
     "Chapter 07", "Present tense",
     "Bias in training data, the hidden labour behind AI, copyright fights, the environmental bill, and who gets a say."),
    ("risk",     "Risk",      "Risk, Safety and Regulation",
     "Chapter 08", "Present tense",
     "Misuse, misinformation, the alignment problem, the debate over existential risk, and how the world is starting to write rules."),
    ("future",   "Future",    "What Happens Next",
     "Chapter 09", "The open questions",
     "The AGI argument, what could still stall progress, and eight honest questions nobody has answered yet."),
]

SLUGS = [p[0] for p in PAGES]
BY_SLUG = {p[0]: p for p in PAGES}

# The chapter path readers follow if they just keep clicking "next".
READING_ORDER = ["home", "origins", "goldenage", "winters", "learning", "deep",
                 "modern", "ethics", "risk", "future", "timeline", "people", "glossary"]


def navbar(active: str) -> str:
    items = []
    for slug, label, *_ in PAGES:
        current = ' aria-current="page"' if slug == active else ""
        items.append(f'        <li><a href="../{slug}/"{current}>{label}</a></li>')
    return "\n".join(items)


def pager(active: str) -> str:
    if active not in READING_ORDER:
        return ""
    i = READING_ORDER.index(active)
    prev_slug = READING_ORDER[i - 1] if i > 0 else None
    next_slug = READING_ORDER[i + 1] if i < len(READING_ORDER) - 1 else None
    parts = []
    if prev_slug:
        parts.append(
            f'      <a class="prev" href="../{prev_slug}/">'
            f'<span class="dir">&larr; Previous</span>'
            f'<span class="ttl">{BY_SLUG[prev_slug][2]}</span></a>')
    if next_slug:
        parts.append(
            f'      <a class="next" href="../{next_slug}/">'
            f'<span class="dir">Next &rarr;</span>'
            f'<span class="ttl">{BY_SLUG[next_slug][2]}</span></a>')
    if not parts:
        return ""
    return ('  <nav class="wrap pager" aria-label="Chapter navigation">\n'
            + "\n".join(parts) + "\n  </nav>\n")


FOOTER_COLUMNS = [
    ("The story", ["origins", "goldenage", "winters", "learning", "deep", "modern"]),
    ("The stakes", ["ethics", "risk", "future"]),
    ("Reference", ["timeline", "people", "glossary"]),
]


def footer() -> str:
    cols = []
    for heading, slugs in FOOTER_COLUMNS:
        links = "\n".join(
            f'            <li><a href="../{s}/">{BY_SLUG[s][2]}</a></li>' for s in slugs)
        cols.append(
            f'        <div>\n          <h4>{heading}</h4>\n'
            f'          <ul>\n{links}\n          </ul>\n        </div>')
    return "\n".join(cols)


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; {site}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#FF0000">
<meta property="og:title" content="{title} &middot; {site}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23FF0000'/><text x='16' y='23' font-family='Helvetica,Arial' font-size='17' font-weight='bold' fill='white' text-anchor='middle'>AI</text></svg>">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main navigation">
      <a class="brand" href="../home/">
        <span class="mark" aria-hidden="true"></span>
        <span class="name">The Machine That <b>Learned</b></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links">Menu</button>
      <ul class="nav-links" id="nav-links">
{navbar}
      </ul>
    </nav>
  </div>
  <div class="read-progress" role="presentation"></div>
</header>

<main id="main">
  <header class="page-head">
    <div class="wrap">
      <p class="kicker"><b>{kicker}</b> &nbsp;&middot;&nbsp; {site}</p>
      <h1>{heading}</h1>
      <p class="years">{years}</p>
      <p class="lede">{description}</p>
    </div>
  </header>

{body}
{pager}</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>{site}</h4>
        <p style="font-size:.92rem;line-height:1.6;max-width:32ch;margin:0">{tagline}</p>
      </div>
{footer}
    </div>
    <div class="footer-bottom">
      <span>Written for readers, not researchers. Every date is checked; every explanation is deliberately plain.</span>
      <span>Built as a static site &mdash; no trackers, no frameworks.</span>
    </div>
  </div>
</footer>

<script src="../assets/js/main.js"></script>
</body>
</html>
"""

REDIRECT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{site}</title>
<meta http-equiv="refresh" content="0; url=home/">
<link rel="canonical" href="home/">
<meta name="description" content="{tagline}">
<style>
  body{{font-family:Helvetica,Arial,sans-serif;background:#fff;color:#0A0A0A;
       display:grid;place-items:center;min-height:100vh;margin:0;text-align:center;padding:2rem}}
  a{{color:#FF0000;font-weight:700}}
</style>
</head>
<body>
  <div>
    <p style="font-size:1.3rem;font-weight:800">{site}</p>
    <p>Redirecting to <a href="home/">the opening chapter</a>&hellip;</p>
  </div>
</body>
</html>
"""


def build() -> None:
    written = []
    for slug, _label, heading, kicker, years, description in PAGES:
        fragment = PAGES_DIR / f"{slug}.html"
        if not fragment.exists():
            raise SystemExit(f"missing content fragment: {fragment}")
        html = SHELL.format(
            title=heading,
            site=SITE_NAME,
            tagline=SITE_TAGLINE,
            description=description,
            kicker=kicker,
            heading=heading,
            years=years,
            navbar=navbar(slug),
            body=fragment.read_text(encoding="utf-8").rstrip() + "\n",
            pager=pager(slug),
            footer=footer(),
        )
        out_dir = ROOT / slug
        out_dir.mkdir(exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        written.append(f"{slug}/index.html")

    (ROOT / "index.html").write_text(
        REDIRECT.format(site=SITE_NAME, tagline=SITE_TAGLINE), encoding="utf-8")
    written.append("index.html")

    # GitHub Pages otherwise skips directories; harmless elsewhere.
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    print(f"built {len(written)} files:")
    for w in written:
        print(f"  {w}")


if __name__ == "__main__":
    build()
