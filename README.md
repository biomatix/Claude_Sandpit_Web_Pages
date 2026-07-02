# Web Pages Harness

A lightweight harness for constructing web pages. Each **job** is a self-contained
page (or small set of pages) with its own brief, assets, and built output.

## Layout

```
.
├── README.md              You are here — how the harness works
├── jobs.md                Registry of all jobs and their status
├── templates/
│   └── job-brief.md       Copy this to start a new job
└── jobs/
    └── <job-name>/        One folder per job
        ├── brief.md       What the page should be (spec / requirements)
        ├── assets/        Source images, fonts, data, references
        └── src/           The built page(s): index.html, css, js
```

## Adding a job

1. Create `jobs/<job-name>/` (kebab-case name).
2. Copy `templates/job-brief.md` to `jobs/<job-name>/brief.md` and fill it in.
3. Add a row to `jobs.md`.
4. Build the page under `jobs/<job-name>/src/`.

## Building & previewing

Pages are plain static files. To preview a job locally:

```powershell
# from the repo root
python -m http.server 8000
# then open http://localhost:8000/jobs/<job-name>/src/
```

## Skills

Installed under `.claude/skills/` (official Anthropic skills):

- **frontend-design** — default for every job. Drives distinctive, intentional
  visual design (palette, typography, layout, motion) so pages don't read as
  templated. Applied automatically when building UI.
- **web-artifacts-builder** — use per-job only when a page needs real
  interactivity (state, routing, shadcn/ui). Scaffolds React + TS + Vite +
  Tailwind + shadcn/ui and bundles to a single HTML file via
  `scripts/init-artifact.sh` and `scripts/bundle-artifact.sh`.

- **clear-writing** (biomatix) — prose collaborator based on Strunk's *Elements of
  Style* and Gastel & Day. Use when drafting/editing page copy for readability.

Also available in-session: **dataviz** (any chart/graph/dashboard work).
