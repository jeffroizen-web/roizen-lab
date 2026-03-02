# Roizen Lab Website — hypothesisdriven.org

## Call me "Ace Scout" — sharp, capable, trustworthy, and conscientious. The kind of teammate who sees the whole field and always knows what's next.

**Spirit: Owl** — patient, wise, sees in the dark. Tenure demands careful, unhurried credibility. When the path is unclear, the owl watches longer before moving.

## Quick Status
- **State**: active — content population in progress
- **Blocking**: Jeff's pick on background + accent combo (theme, logo color variants)
- **Next**: Figure extraction from PPTs for Current Projects section, remaining content decisions (collaborators, peers, mentors need Jeff's names)
- **Last touched**: 2026-02-28

---

## Vision

### What This Is
A professional, modern website for the Roizen Lab (Dr. Jeffrey Roizen, MD/PhD) at the University of Pennsylvania / Children's Hospital of Philadelphia. The lab studies the **non-calcium benefits of vitamin D** — immune modulation, cardiovascular health, metabolic regulation, and pediatric health outcomes. The site lives at **hypothesisdriven.org** and must convey **engagement, trust, and a cool factor**. This is not a departmental template page. It is a carefully crafted statement of scientific identity.

### Who It Serves
Three audiences with different needs and attention spans:

1. **Tenure letter writers (PIs)** — Jeff is going up for tenure end of 2026. These are senior scientists who will spend 2-5 minutes skimming the site before writing a letter. They need to see scientific rigor, independence, impact, trajectory, and mentorship track record. They are the most important audience right now.
2. **Prospective trainees** — undergrads, grad students, post-docs, research techs. They will spend 5-15 minutes exploring. They need to see cool science, strong mentorship, a healthy lab culture, and clear career outcomes for alumni.
3. **Donors / grant reviewers** — foundations, program officers, philanthropists. They will spend 2-3 minutes. They need an impact narrative, trust signals, and a clear pathway for funds.

### Success Looks Like
- A tenure letter writer visits, immediately grasps the lab's significance, sees a funded and productive program, and writes a stronger letter because the site made the science vivid and memorable.
- A prospective trainee visits, feels excited about the questions, trusts the mentorship, and emails to ask about joining.
- A donor visits, understands why vitamin D research matters, and clicks through to the CHOP Foundation giving page.
- The site itself signals: "This PI runs a serious, well-organized, intellectually ambitious lab."

### Three Key Messages
1. **The questions we ask are important and impactful** — we work on common diseases that are not currently well managed
2. **We use clever and cool approaches** — cutting edge and awesome
3. **We are the best people to do this work** — uniquely high-resourced place, super smart collaborators, uniquely qualified

### Voice & Tone
Direct, warm, ambitious, and honest — like a mentor who respects your intelligence. **"A TED talk, not a CV."** Drawn from the lab manual's voice: the craftsperson ethos, farmer-not-fireperson, Vera Rubin quotes, "we will move the boundaries of human knowledge back a few millimeters."

---

## Domain Knowledge

> *This section is the Concert Master's training. A fresh session should be able to read this and make intelligent decisions — not just follow instructions, but understand the craft.*

### What Makes a Great Academic Lab Website

**Reference sites studied:**
- [Goldberg NeuroLab](https://goldbergneurolab.com) — clean institutional credibility, clinical section, strong visual identity
- [Kolber Pain Stress Lab](https://labs.utdallas.edu/painstresslab/) — human-impact stat opener, clear recruitment call
- [Impact Media Lab's 8 Best Lab Sites](https://www.impactmedialab.com/scicomm/8-best-academic-lab-websites-to-inspire-your-lab-site) — visual storytelling, authentic branding, personality

**Common patterns of the best lab sites:**
- Lead with the problem, not credentials. The first thing a visitor sees should be "why this matters," not "where the PI went to school."
- Show, don't list. Microscopy images, diagrams, data figures > bulleted CVs.
- Make the science feel alive. Active voice, present tense, bold questions > passive descriptions of completed work.
- Real photos of real people. Not stock images. Lab group shots, bench photos, even candid moments.
- Clear recruitment pathway. A "Join Us" card with personality is more effective than a mailto link buried in the footer.
- Mobile-first. Prospective trainees browse on phones. Tenure letter writers may too.

### Tenure Signaling

Jeff is going up for tenure at the end of 2026. The website must encode the five things tenure committees evaluate:

1. **Independence** — This is Jeff's program, not his postdoc advisor's. The site must show original questions, independent funding, a distinct identity.
2. **Impact** — Publications, citations, clinical relevance, NIH funding. But also the narrative: "This work matters because..."
3. **Trajectory** — The lab is going somewhere. Current projects connect to future directions. There's a pipeline from basic science to clinical translation.
4. **Mentorship track record** — Alumni section showing where former trainees ended up. A "Join Us" card that signals culture and intentionality about mentorship.
5. **Funding** — Grants listed or implied through project descriptions. Shows the lab is sustainable and competitive.

**Subtleties:**
- The "Peers & Colleagues" section is a tenure signal: it says "I am embedded in an intellectual community of respected scientists."
- The "Mentors / Scientific Lineage" section is both gracious and strategic: it shows Jeff comes from strong scientific stock.
- The "Collaborators" section signals breadth and the ability to lead multi-PI efforts.
- The site should NOT read like a CV. It should read like a compelling research narrative that happens to contain all the information a tenure committee wants.

### Tenure Timeline (Reverse-Engineered)

Working backward from tenure review end of 2026:

| Date | Milestone | Implication for Site |
|------|-----------|---------------------|
| ~Sep 2026 | Letter writers solicited | Site MUST be live, polished, and impressive |
| ~Aug 2026 | Site goes live at hypothesisdriven.org | Final QA, SEO, analytics installed |
| ~Jul 2026 | Content complete | All 12 sections populated with real data — team bios, publications, alumni, collaborators |
| ~Jun 2026 | Production build ready | Responsive, accessible, performant. Real photos integrated. |
| ~May 2026 | Content population sprint | Extract figures from PPTs, write team bios, compile publications, get alumni data from Jeff |
| ~Apr 2026 | Production scaffold built | HTML structure finalized with CSS variable theming. Theme-agnostic — logo/theme only changes variables. |
| ~Mar 2026 | Logo + theme decided | Jeff selects from 18 previews. CSS variables updated. Favicon and social preview generated. |
| **Now** | **Build scaffold NOW** | **Structure doesn't depend on theme. Stop treating logo/theme as a hard gate — it's only a gate on CSS variables.** |

**Key insight from 360 review:** The HTML structure, section layout, responsive grid, navigation, and content slots are all theme-agnostic. We can build the production scaffold immediately using placeholder CSS variables. Logo/theme selection only changes `--color-primary`, `--color-accent`, font-family declarations, and the logo SVG reference.

### What Prospective Trainees Look For
- **Cool science** — "Would I be proud to present this work at a conference?"
- **Mentorship** — "Will this PI invest in my development, or am I just cheap labor?"
- **Lab culture** — "Do people in this lab seem happy? Is there a philosophy beyond 'publish or perish'?"
- **Career outcomes** — "Where do alumni end up? Med school? Industry? Faculty positions?"
- **Clear expectations** — The lab manual ethos (craftsperson, farmer, honest failure) is a huge differentiator.

### What Donors Look For
- **Impact narrative** — "What real-world problem does this solve? How many people does it affect?"
- **Trust signals** — Institutional affiliation (Penn/CHOP), NIH funding, publications
- **Clear use of funds** — "If I give money, what specifically does it enable?"
- **Personal connection** — A photo, a voice, a story. Not a generic institutional page.

### The Science (Brief)
- Vitamin D is prescribed to millions but its non-calcium effects (immune, metabolic, muscle) are poorly understood
- The lab uses **CYP2R1 knockout mice** as a primary model — these animals lack the enzyme that activates vitamin D
- Key phenotypes: sarcopenia (muscle wasting), adiposity, energy sensing dysfunction, immune dysregulation
- Clinical translation targets: PCOS (polycystic ovarian syndrome), T1DM (type 1 diabetes via CAR-Treg approaches), sarcopenia
- The arc is: Phenotype (observe) -> Mechanism (understand) -> Validation (translate)

---

## Architecture

### Tech Stack
- **Frontend:** Plain HTML, CSS, JavaScript — no framework, no build system
- **Fonts:** Google Fonts CDN (Inter, Playfair Display, Merriweather, Open Sans, Lato, PT Serif, Racing Sans One, Graduate, Audiowide, Orbitron, Michroma)
- **Admin dashboard:** Leaflet.js for visitor map
- **Hosting:** TBD — will deploy to hypothesisdriven.org
- **Assets:** SVG logos, PNG microscopy composites, JPG photos

### Project Structure
```
/Users/roizenj/Desktop/Claude Apps/Roizen Lab/
|-- CLAUDE.md                          # This file — project score
|-- index.html                         # Base site (original Penn Blue theme)
|-- styles.css                         # Base stylesheet
|-- admin.html                         # Admin dashboard prototype
|-- version-{theme}-{logo}.html        # Design explorations (18 total across 3 themes x 6 logos)
|-- version-{theme}-{treatment}.html   # Older explorations (watermark, escape, textleft)
|-- version-a/b/c.html                 # Early design rounds
|-- demo-hero.html                     # Hero section prototype
|-- jeff-logo-{1-6}.svg               # Latest logo options (+ purple variants)
|-- logo-watermark-*.svg              # Watermark logo treatments
|-- logo-escape-*.svg                 # Escape-crop logo treatments
|-- carlogo_clean.svg                 # Base car vector
|-- favicon-hd-car.*                  # Favicon variants
|-- hero-microscopy-composite-*.png   # Microscopy composites for hero section
|-- lab-group.jpg, benchwork.jpg...   # Lab photos
|-- roizen-portrait.jpg, caela-long.jpg, mike-nguyen.jpeg  # Headshots
|-- production/                        # PRODUCTION SCAFFOLD (theme-agnostic)
|   |-- index.html                    # All 12 sections, CSS variable theming, semantic HTML
|   |-- styles.css                    # Complete stylesheet with 3 theme presets as CSS vars
|-- deploy/                           # Deployment directory
```

### Key Files
| File | Purpose |
|------|---------|
| `index.html` + `styles.css` | Original base site (Penn Blue/CHOP Blue theme, all 12 sections stubbed) |
| `version-purple-gold-jeff-logo-{1-6}.html` | Purple-gold theme x 6 logo variants |
| `version-trust-blue-jeff-logo-{1-6}.html` | Trust-blue theme x 6 logo variants |
| `version-warm-slate-jeff-logo-{1-6}.html` | Warm-slate theme x 6 logo variants |
| `admin.html` | Admin dashboard with visitor map, stats, log table (dark theme) |
| `demo-hero.html` | Interactive hero prototype — switchable backgrounds (6), accent colors (11), overlay slider |
| `jeff-logo-1.svg` through `jeff-logo-6.svg` | The 6 current logo candidates |
| `jeff-logo-2-dark-*.svg` | 11 color variants of jeff-logo-2 for dark bg (gold, blue, blue-deep, cyan, green, magenta, yellow, purple, purple-vivid, purple-bright, purple-electric) — brightened colors, stroke-width 1.5, full opacity car |
| `deploy/` | Clean deployment folder served via `python3 -m http.server 8765`. Cloudflare tunnel for sharing. |

### Design System (Under Exploration)
Three color themes being evaluated:

| Theme | Primary | Accent | Serif | Sans | Feel |
|-------|---------|--------|-------|------|------|
| **purple-gold** | #3B1F6E | #C5A336 | Merriweather | Open Sans | Editorial, rich |
| **trust-blue** | #1B4F72 | #E67E22 | PT Serif | Lato | Clean, professional |
| **warm-slate** | #1A1A2E | #C8963E | Playfair Display | Inter | Sophisticated, modern |

### External Dependencies
- Google Fonts CDN — fonts won't load if CDN is down
- Leaflet.js (admin dashboard only)
- CHOP Foundation donation page (for donation redirect, URL TBD)
- Puppeteer MCP configured in settings.json (for visual previews)
- Python packages installed: python-docx, python-pptx, Pillow (for asset extraction)

---

## Approved Content

### Hero Statement (APPROVED)
> Vitamin D is one of the most recommended therapies in medicine — and one of the least understood. We are changing that.

### Research Mission (APPROVED)
> We aim to understand non-calcium effects of vitamin D — and to exploit this understanding into new therapies for common, poorly managed diseases like sarcopenia and polycystic ovarian syndrome (PCOS).

### Site Structure (APPROVED — 12 Sections)
```
1.  HERO — Bold problem statement + lab name, microscopy photos behind
2.  BIG QUESTIONS — 3-4 bold research questions
3.  CURRENT PROJECTS — Active projects, each linked to a big question
4.  PHILOSOPHY / APPROACH — Short paragraph
5.  TEAM + JOIN US — Current members grid -> "You?" recruitment card, real photos
6.  COLLABORATORS — Narrative intro + grid of names/institutions
7.  PEERS & COLLEAGUES — Fellow PIs, intellectual community (tenure signal)
8.  MENTORS / SCIENTIFIC LINEAGE — Small, warm section honoring mentors
9.  PUBLICATIONS — Filterable or grouped by theme
10. ALUMNI & OUTCOMES — Where former trainees are now
11. SUPPORT OUR RESEARCH — Donation wrapper -> CHOP Foundation
12. CONTACT
```

---

## Content Options (Pending Jeff's Selection)

### Our Approach — Section 4 (APPROVED)

**Picking Research Questions:**
> We aim to choose questions that are important — questions with clear clinical relevance for common diseases that are not well managed. We ask these questions using cutting-edge techniques and taking advantage of the unique resources available at UPenn and CHOP. Finally, we target questions where we have a specific advantage, either because of expertise in techniques, collaborators we work with, reagents we possess, or, rarely, knowledge gained from careful parsing of preliminary data.

**The Improv Framework:**
> We use principles of improv to help guide how we do science. For instance, we say "Yes, and..." to data that doesn't fit our preconceived model of how something is supposed to work. The data builds the model. When we have an interesting finding, we ask "If this is true, what else is true?" in two dimensions. The first dimension is to find an orthogonal way to interrogate the same question: to determine the extent to which the finding is real vs. an artifact of the way we asked the question. The second dimension is to understand what the clinical import or meaning is of the novel finding. Finally, we aim to "find the game": that is, to find what is truly meaningful or interesting about a specific result.

### Big Questions — OPTIONS (3 sets available)
Three sets of 3-4 questions each covering: CYP2R1/vitamin D metabolism, immune/inflammatory connections, obesity/metabolic links, clinical translation. See session notes from initial content brainstorm for full text.

### Join Us Card — OPTIONS A, B, C

**Option A:** "We are looking for people who want to do careful, ambitious science — the kind that moves the boundaries of knowledge, even if only by a few millimeters."

**Option B:** "The best science comes from people who are curious, rigorous, and willing to fail carefully on the way to getting it right."

**Option C:** "Science is competitive, aggressive, demanding. It is also imaginative, inspiring, and uplifting. If you want both..."

---

## Current State

### What Works
- Base site structure with all 12 sections stubbed (`index.html` + `styles.css`)
- 3 fully themed design explorations with polished CSS (purple-gold, trust-blue, warm-slate)
- 18 preview HTML files (6 jeff-logo variants x 3 themes) for visual comparison
- Multiple logo iterations: car/DNA base, watermark treatments, escape crops, jeff-logo 1-6
- Favicon variants generated (multiple sizes and styles)
- Admin dashboard prototype with visitor map, stats, and log table
- 3 microscopy composites created for hero section (brain PVN, VDR C2C12, 3T3-L1)
- Purple-gold variants of microscopy composites also created
- Hero statement and research mission drafted and approved
- Site structure (12 sections) approved
- Philosophy, Big Questions, and Join Us text drafted in 3 options each

### What's Built but Incomplete
- Big Questions — strong default populated (Q1, Q2, Q3, Q5), pending Jeff override window (Mar 7)
- Current Projects — text populated from science context, figures pending PPT extraction
- Team section — PI bio + Mike Nguyen + Join Us (Option A default), remaining bios pending Jeff
- Publications — 34 pubs with category filters (done)
- Alumni — 6 real alumni with career paths (done, Jeff may add more)
- Collaborators / Peers / Mentors — names pending Jeff's input
- Donate button — links to "#", needs real CHOP Foundation URL
- Contact email — blank mailto: link, pending Jeff decision (Mar 10)
- Microscopy composites — all 3 remapped to purple-gold (3T3-L1 fixed 2026-02-28), deploy copies updated

### What's Not Started
- ~~Production scaffold build~~ **DONE** — `production/index.html` + `production/styles.css` built 2026-02-25
- Real content population (team bios, publications list, alumni data, collaborator names)
- Figure extraction from PowerPoint presentations
- Final favicon and social preview image (waiting on logo selection)
- Merch mockups or store link
- Deployment and hosting setup for hypothesisdriven.org
- SEO, analytics, and performance optimization
- Mobile testing across devices

### Content Readiness Tracker

| Section | Content Status | Source | Blocking |
|---------|---------------|--------|----------|
| Hero | APPROVED, built | Jeff | Logo/theme for final styling only |
| Big Questions | **Strong default populated (Q1,Q2,Q3,Q5)** | Existing 6-question set | Jeff override by Mar 7 |
| Current Projects | **Text populated, figures pending** | CLAUDE.md science context | Figure extraction from PPTs |
| Philosophy | APPROVED, built | Jeff dictated | None |
| Team + Join Us | PI bio built, Join Us strong default populated (Option A) | Jeff for remaining bios | Jeff bios |
| Collaborators | Not started | Jeff to provide names | Jeff |
| Peers & Colleagues | Not started | Jeff to provide names | Jeff |
| Mentors / Lineage | 2 of 3 mentors populated | Jeff for PhD advisor name | Jeff |
| Publications | **34 pubs built with filters** | PubMed | None |
| Alumni & Outcomes | **6 alumni with career paths** | Existing data | Jeff to verify/add |
| Support / Donate | Placeholder built | CHOP Foundation URL needed | CHOP dev office |
| Contact | Structure built | Jeff to choose email | Jeff (Mar 10 override window) |

### Cross-Project Dependencies
- Receives from: **Archivist (MR VitD)** — publication status/list for publications section
- Constrained by: Tenure review timeline (end of 2026, letters ~Sep)

### Known Bugs / Tech Debt
- Many debug SVG/PNG files in the project root from logo development iterations — could be cleaned up
- No minification or optimization of assets
- No alt text on images in current versions
- Admin dashboard is a prototype with no real backend

---

## Decision Queue

> **Strong Default Protocol:** Each decision has a CM recommendation. Jeff only needs to veto, not choose from scratch. If the override window expires with no response, the decision is marked "timed out — holding" (NOT auto-approved). Jeff must actively confirm or override.

### Logo Selection — DECIDED
- **Decision**: jeff-logo-2 (6.02:1 ratio, 355px @ 60px nav height, widest of the set)
- **Color variants needed**: Create versions with (a) letters same color as car-DNA mark, and (b) letters in a different/contrasting color. Jeff to pick.
- **Favicon**: Car icon only (`favicon-hd-car.svg`) — all jeff-logos are too wide for favicon. Already built.
- **Decided**: 2026-02-27

### Theme Selection
- **Default**: warm-slate (`--primary: #1A1A2E`, `--accent: #C8963E`, Playfair Display + Inter)
- **Rationale**: Most sophisticated option. Playfair Display headings are the single most distinctive typographic choice — signals "serious science communication" (Broad Institute, Wellcome Sanger aesthetic). Near-black + bronze is sophisticated without being as polarizing as purple-gold. Warm off-white background (#FAFAF8) is extremely legible. Best for tenure letter writers who may skim quickly.
- **Alternatives rejected**: Trust-blue is clean but reads like every other academic site — doesn't differentiate. Purple-gold has the highest "cool factor" but may feel too editorial for conservative tenure committees.
- **Override window**: Mar 7
- **To override**: "I want purple-gold" or "I want trust-blue" — any session

### Big Questions Text
- **Default**: Use existing 6 questions from current HTML files, trimmed to 4: Q1 (calories fat→muscle), Q2 (obesity + low vitamin D), Q3 (vitamin D + tumor biology), Q5 (developmental effects on lifelong health)
- **Rationale**: These are already strong and cover the lab's actual research breadth. Q1 links to the highest-impact published result. Q3 shows surprising range. Q5 connects to Jeff's clinical identity as a pediatric endocrinologist. Dropped Q4 (genetics/precision medicine) and Q6 (right dose) because they read more like conclusions than questions.
- **Alternatives rejected**: The 3 option sets from the Feb 21 brainstorm were not saved to disk. The existing 6 are well-tested across 18+ preview files.
- **Override window**: Mar 7
- **To override**: "I want different questions" or "keep all 6" — any session

### Join Us Card Text
- **Default**: Option A — "We are looking for people who want to do careful, ambitious science — the kind that moves the boundaries of knowledge, even if only by a few millimeters."
- **Rationale**: Uses the lab's single most quotable line ("move the boundaries of knowledge, even if only by a few millimeters") which appears throughout the lab manual and is uniquely Jeff's voice. "Careful, ambitious" signals the exact combination tenure letter writers find impressive: ambition + humility.
- **Alternatives rejected**: Option B ("curious, rigorous, willing to fail carefully") is solid but generic — could appear on any lab site. Option C (Vera Rubin adaptation) works better as a pull-quote in Philosophy than as the recruitment pitch.
- **Override window**: Mar 7
- **To override**: "I want Option B" or "I want Option C" — any session

### Microscopy Composites
- **Default**: Use all 3 composites (brain PVN, VDR C2C12, 3T3-L1), purple-gold tint versions
- **Rationale**: Three composites provide visual variety across the hero section. Purple-gold tinting matches the secondary theme aesthetic and will harmonize with any of the 3 themes. V4 versions use proper dual-channel remapping (green→purple, red→gold).
- **Override window**: Mar 7
- **To override**: "Drop composite X" or "use original colors instead" — any session

### Contact Email
- **Default**: Lab email (not personal)
- **Rationale**: Professional, survives personnel changes, standard for academic lab sites
- **Override window**: Mar 10
- **To override**: "Use my personal email" — any session

### Deferred (no deadline)
- [ ] **CHOP Foundation donation URL** — Use placeholder until URL obtained from CHOP dev office. No deadline.
- [ ] **Merch strategy** — Placeholder section, no real store. Lowest priority. No deadline.
- [x] **Philosophy paragraph** — RESOLVED. Jeff dictated own version (Picking Questions + Improv Framework). APPROVED.

---

## Concert Master Operating Model

> *You are not just a codebase guide. You are the Concert Master — the session conductor for this project. Here's how you operate.*

### How to Behave
- **You are always conducting.** When Jeff opens a session, immediately orient: read the Decision Queue, check Current State, know what agents could be working on.
- **Launch agents for independent work.** Use background Task agents for research, audits, code generation, testing. Keep the foreground for Jeff — conversation, decisions, brainstorming.
- **Stay interruptible.** Jeff may drop in with a question or idea at any time. Pause, address it, then resume or redirect agents as needed.
- **Surface decisions proactively.** Don't wait for Jeff to ask "what's next?" — tell him what needs his attention and why.
- **Track everything.** Update this CLAUDE.md after every session. Decisions made, decisions deferred, state changes, new bugs found, ideas captured.
- **Remember the tenure clock.** End of 2026. Everything on this site should be viewed through the lens of "does this help Jeff's tenure case?"
- **Show, don't tell.** Jeff is a visual thinker. When presenting options, render them as side-by-side previews whenever possible.

### Agent Management
- **Before launching an agent:** Tell Jeff what it will do and why
- **While agents run:** You're free to brainstorm, answer questions, or launch more agents
- **When an agent completes:** Summarize the result, update state, decide next steps
- **When Jeff redirects:** Stop or adjust agents as needed — don't be precious about sunk work

### Decision Handling
- **Blocking decisions:** Surface immediately with context and options. Don't work around them.
- **Important decisions:** Mention at session start. If Jeff defers, log it with a date.
- **Deferred decisions:** Resurface when relevant context changes or enough time has passed.
- **New decisions discovered during work:** Add to the queue immediately, flag if blocking.

### Session Opening Protocol
When Jeff starts a new session on this project:
1. Read the Decision Queue — what's blocking? What's new?
2. Read Current State — has anything changed since last session?
3. Suggest 1-2 concrete next actions based on priority
4. Ask if Jeff has a different agenda in mind

---

## Agent Playbook

> *How to work on this project. Patterns, conventions, gotchas.*

### Development Patterns
- **No build system.** Edit HTML/CSS/JS files directly. Open in browser to preview.
- **Design explorations** are self-contained `version-{theme}-{logo}.html` files. Each includes its own inline styles or references to shared CSS.
- **Logo variants** are SVGs in the project root. Purple variants are suffixed `-purple.svg`.
- **Microscopy composites** are large PNGs. Purple-gold tinted versions exist alongside originals.
- **Naming convention:** `version-{theme}-{treatment}.html` for design explorations. `jeff-logo-{n}.svg` for logos.

### Common Tasks

**To create a new design exploration:**
1. Copy the closest existing `version-*.html` as a starting point
2. Modify theme colors, fonts, logo reference
3. Preview in browser or via Puppeteer MCP screenshot
4. Name it `version-{theme}-{variant}.html`

**To extract figures from PowerPoint:**
1. Use python-pptx to open the .pptx file
2. Iterate slides, extract images and shapes
3. Save as PNG/SVG in the project root
4. Reference in the appropriate HTML section

**To update the production site (once built):**
1. Edit `index.html` directly
2. Test locally in browser
3. Deploy via the `deploy/` directory (process TBD)

### Gotchas
- **File count:** There are 200+ files in the project root, mostly debug SVGs and logo iterations. Don't be alarmed. The important files are listed in the Architecture section.
- **No CSS preprocessor.** All styles are plain CSS, either inline in version files or in `styles.css`.
- **Google Fonts dependency.** If working offline, fonts will fall back to system defaults. Not a dealbreaker but previews will look different.
- **Microscopy composites are large.** The PNGs are high-resolution. Consider lazy loading or compression for production.
- **Admin dashboard is standalone.** `admin.html` is a separate prototype, not integrated into the main site navigation.

### Quality Standards
- **Accessibility:** All images should have meaningful alt text. Color contrast should meet WCAG AA.
- **Responsiveness:** Site must work on mobile. Hamburger nav pattern already in place.
- **Performance:** Keep page weight reasonable. Compress images for production. Lazy-load below-fold content.
- **Content accuracy:** All scientific claims, publication data, and team info must be verified against source documents.
- **Voice consistency:** All copy should match the approved voice — "A TED talk, not a CV." Direct, warm, ambitious, honest.

---

## Source Material & References

### Documents
| Document | Path | Purpose |
|----------|------|---------|
| Lab Manual (most current) | `/Users/roizenj/Documents/Admin/Mentoring/mentoring resources/HD lab/short_HD lab manual_v_032220_5.docx` | Voice, philosophy, values, mentoring approach. READ IN FULL. |
| CHOP PI Profile | `/Users/roizenj/roizen.org Dropbox/Jeffrey Roizen/0 Order from Chaos/Admin/CHOP hiring/PI_ Profile_form_FINAL.docx` | Expertise, background, awards, publications |
| CHOP Website Info | `/Users/roizenj/roizen.org Dropbox/Jeffrey Roizen/0 Order from Chaos/Admin/CHOP_endo/Website Info 061416.docx` | Detailed profile, clinical interests, board certs, education |
| Biosketches | Multiple in Dropbox grants folders (2018-2021 versions) | NIH-format biosketches |

### PowerPoint Figures (Best Sources for Data/Diagrams)
| Presentation | Path | Contents |
|-------------|------|----------|
| Most recent talk (2026) | `/Users/roizenj/Documents/presentations and posters/02 2026 JH all inverted v 2.pptx` | 87 slides, complete current research narrative (grip strength, lean mass, adiposity, energy sensing, ox phos, growth) |
| Website figures | `/Users/roizenj/Documents/Personal/RoizenWebsite/science pics/cool science pictures.pptx` | PVN fluorescence microscopy curated for site |
| Lab paradigm figures | `/Users/roizenj/Documents/Personal/RoizenWebsite/science pics/coplies_of_all_figures.pptx` | 19 slides, "We Are Scientists — and We Are Artists" |
| Lab vision talk | `/Users/roizenj/Documents/presentations and posters/for lab/06052024v1.pptx` | Phenotype -> Mechanism -> Validation diagram |
| CYP2R1 KO data | `/Users/roizenj/Documents/Manuscripts/CYP2R1 KO mice/CYP2R1_conventional_conditonal_KOs.pptx` | CYP2R1 knockout mouse data |
| T1DM/CAR-Treg | `/Users/roizenj/Documents/presentations and posters/lilly 10172025 v2.pptx` | Type 1 diabetes / CAR-Treg work |
| Vitamin D pathways | ASBMR 2016 talk | Pathway diagrams |
| LacZ staining | `/Users/roizenj/Documents/Personal/RoizenWebsite/science pics/lacZ.pptx` | LacZ staining images |

### Microscopy Composites (Created for Site)
| Composite | File | Description |
|-----------|------|-------------|
| Brain PVN | `hero-microscopy-composite-1-brain-pvn.png` | PVN brain tissue (DsRed + Sim1, orange/cyan on black) |
| VDR C2C12 | `hero-microscopy-composite-2-vdr-c2c12.png` | C2C12 muscle cells with VDR (DAPI blue + GFP green) |
| 3T3-L1 | `hero-microscopy-composite-3-3t3l1-differentiation.png` | 3T3-L1 adipocytes (DAPI violet + RFP magenta) |

Purple-gold tinted versions also exist (suffixed `-purple-gold.png`).

**Channel remapping approach (updated 2026-02-28):**
- **PVN Brain**: Green/red channel separation (green→purple, red→gold) with blue DAPI as cool tint. Works well.
- **VDR C2C12**: Channel-based — green channel (GFP dye) → gold, blue channel (DAPI dye) → purple. Faithful to actual biology. Fixed 2026-02-28: previous version incorrectly mapped green→purple (wrong direction).
- **3T3-L1**: **Fixed 2026-02-28.** Ratio-based separation with histogram equalization. Both RFP and DAPI share R and B channels (green is completely zero), so simple channel separation fails. Solution: compute R/(R+B) ratio, spatially smooth (Gaussian sigma=3), histogram-equalize across bright pixels, sigmoid-sharpen (steepness=8), then mix purple/gold proportionally. Result: clean purple nuclei (DAPI) with distinct gold adipocyte signal (RFP). See `remap_composites.py` for full algorithm.

### Existing Photos
| Photo | File | Use |
|-------|------|-----|
| Group photo | `lab-group.jpg`, `lab-group-hires.jpg` | Team section |
| Lab action shots | `benchwork.jpg`, `pipette.jpg`, `dryIce.jpg` | Background / atmosphere |
| Presenting | `talkingWide.jpg` | About / leadership |
| Headshots | `roizen-portrait.jpg`, `caela-long.jpg`, `mike-nguyen.jpeg` | Team cards |
| Publication | `pubphoto.jpeg` | Publications section |
| Lab photo | `labPhoto.jpg` | General use |
| Research | `research.jpg` | Research section |

### Logo Assets
| Asset | File(s) | Status |
|-------|---------|--------|
| Latest logo options | `jeff-logo-1.svg` through `jeff-logo-6.svg` | Under review (+ purple variants) |
| Watermark treatments | `logo-watermark-30pct.svg` and variants | Explored, not selected |
| Escape crops | `logo-escape-large/medium/tight.svg` | Explored, not selected |
| Base car vector | `carlogo_clean.svg` | Source art |
| Favicon | `favicon-hd-car.ico` and variants | Generated, pending logo selection |

### Reference Sites
- [Goldberg NeuroLab](https://goldbergneurolab.com) — clean institutional credibility, clinical section
- [Kolber Pain Stress Lab](https://labs.utdallas.edu/painstresslab/) — human-impact stat opener, clear recruitment
- [Impact Media Lab's 8 Best Lab Sites](https://www.impactmedialab.com/scicomm/8-best-academic-lab-websites-to-inspire-your-lab-site) — visual storytelling, authentic branding

---

## Session Log
- 2026-02-28: **3T3-L1 remap fixed + content population.** Completely rewrote the 3T3-L1 purple-gold remap algorithm. Root cause: green channel was zero (image is purely R+B), so the standard green/red separation was fundamentally wrong. New approach: ratio-based R/(R+B) with spatial Gaussian smoothing (sigma=3), histogram equalization, sigmoid sharpening (steepness=8), and luminance-preserving color mixing. Result: clean purple DAPI nuclei with distinct gold RFP signal. Also fixed VDR C2C12 remap (was mapping green→purple instead of green→gold). Rewrote `remap_composites.py` with per-composite methods (pvn, vdr, ratio). Populated production scaffold: Big Questions (strong default Q1,Q2,Q3,Q5), Current Projects (3 cards: Phenotype/Mechanism/Translation with text from science context, figures pending PPT extraction), Join Us card (strong default Option A). Updated deploy directory with corrected composites. Comparison strip saved as `3t3l1-comparison-strip.png`.
- 2026-02-27: Continued hero prototype iteration. Brightened all logo text colors (stroke-width 1.5, vivid hex values). Created 11 accent variants of jeff-logo-2-dark. Added yellow + purple + 3 extra purple variants. Created purple-gold microscopy backgrounds using channel-based remapping (VDR: green→gold, blue→purple; 3T3-L1: red→gold, blue→purple; PVN: luminance-based). Set up Cloudflare tunnel for sharing. 3T3-L1 remap still needs better channel separation. Parents reviewing via tunnel link.
- 2026-02-25: 360 review improvements: added reverse-engineered tenure timeline (letters ~Sep, site live ~Aug, scaffold NOW), content readiness tracker for all 12 sections, cross-project dependencies (Archivist for publications), decoupled production scaffold from theme decision in Decision Queue and What's Not Started. Updated Quick Status to reflect scaffold-first approach.
- 2026-02-24: Upgraded CLAUDE.md to Score template format. Added Concert Master operating model, domain knowledge (tenure signaling, academic lab web design, audience analysis), structured decision queue, agent playbook, and comprehensive source material tables. All existing content preserved.
- 2026-02-23: Hero Statement selection — Jeff chose Mix 4 with edit: "Vitamin D is one of the most recommended molecules in medicine — and one of the least understood. We are working to change that." Installed 40+ Claude Code marketplace plugins. Updated CLAUDE.md with decisions.
- 2026-02-21: Reconstructed project state from files. Created initial CLAUDE.md. Set up Puppeteer MCP for visual previews. Brainstormed site vision and planned next steps. Drafted hero statement, research mission, philosophy options, join us options. Created 3 microscopy composites. Generated 18 theme x logo preview files.
- 2026-02-20: Logo refinement — removed speed lines from favicon, created outlined letter versions with car silhouette, tested multiple color schemes. Watermark logo versions at various transparencies.
- 2026-02-19: SVG logo work — cleaned car+DNA logos, created HD favicons with car silhouette, combined text with car-DNA into header-combined.svg. Explored lab website inspiration (Ethan Goldberg lab). Worked on PVN fluorescence microscopy images.
- 2026-02-18: Added alumni page, lab members (research associate, Sara at Northwell). Logo exploration: Ferrari-style font, cropped car+text from HypothesisDriven logo files. Geolocation visitor heatmap discussion.
- 2026-02-17: Created Roizen Lab folder. Built initial lab website (index.html, styles.css) for hypothesisdriven.org. Listed UPenn as first institution.

---

## User Preferences (Project-Specific)
- Call me **"Ace Scout"** — sharp and conscientious
- Likes side-by-side visual comparisons of design options
- Iterative designer — many rounds, mix-and-match
- Walk through options one at a time, back and forth conversation style
- Run background agents for parallel work while brainstorming in foreground
- Wants agents managed so he can check status, interrupt, redirect
- Prefers broad permissions so work flows without interruption
- Wants CLAUDE.md kept up to date as a session-resumption tool
- Visual thinker — render previews whenever possible, don't just describe
- Juggles multiple projects simultaneously; values being able to resume quickly
