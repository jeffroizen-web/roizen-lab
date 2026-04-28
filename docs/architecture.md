# Ace Scout (Roizen Lab) — Architecture

## Tech Stack
- **Approach**: No build system — plain HTML/CSS/JS, edit directly, preview in browser
- **Working file**: `compare-purple-gold.html` (active development)
- **Production scaffold**: `production/` directory
- **Domain**: hypothesisdriven.org (not yet deployed)
- **Decision journal**: `python3 ~/Desktop/"Claude Apps"/"Claude coding Asst"/decision_journal.py`

## Design System
- **Primary color**: `--primary: #3B1F6E` (purple)
- **Accent color**: `--accent: #C5A336` (gold)
- **Layout**: Ethan Goldberg-style dual header
  - Dark purple institution bar: CHOP + CHOP RI (left), Penn Medicine (right)
  - 1px gold border-bottom (`var(--accent)`)
  - White nav bar: Jeff's logo + nav links
- **Logo**: `jeff-logo-2-theme-purple.svg` (55px height, `shape-rendering: geometricPrecision`)
- **Favicon**: `favicon-hd-car.svg` (car icon only, logos too wide)
- **Hero heading**: "Redefining Vitamin D"

## Directory Structure
```
compare-purple-gold.html   # Active working file
production/                 # Production scaffold
extracted-figures/
  curated-for-website/      # 30 figures from PPT (7 primary q1-q7 + 23 bonus)
photos/                     # Lab and people photos
docs/
  score_reference.md        # Deep context (vision, domain, architecture)
```

## Key Design Decisions
- **No build system**: Plain HTML/CSS/JS keeps things simple, directly editable, and avoids toolchain complexity for a mostly-static academic website
- **200+ files in root**: Mostly debug SVGs and logo iterations from design exploration
- **Responsive**: Breakpoints for tablet, phone, and very small phone

## Three Audiences
1. **Tenure letter writers (PIs)** — 2-5 min skim, need to see rigor/impact/trajectory
2. **Prospective trainees** — 5-15 min explore, need cool science + mentorship signals
3. **Donors / grant reviewers** — 2-3 min, need impact narrative + trust signals

## Cross-Project Dependencies
- **From Archivist**: Publication list for the publications section
- **Tenure deadline**: End of 2026. Letters solicited ~Sep 2026. Site must be live and polished by Aug 2026.
