# navinsridhar.github.io — personal website

Personal academic website for **Navin Sridhar** (KIPAC, Stanford), built on
[al-folio](https://github.com/alshedivat/al-folio) (Jekyll). The CV is
auto-synced from Overleaf nightly via GitHub Actions.

---

## what's in this repo

```
.
├── _config.yml                  # site-wide settings, plugins, scholar config
├── Gemfile                      # Ruby gems al-folio needs
├── _pages/                      # the pages that show up in the navbar
│   ├── about.md                 # landing page (/) — bio, profile, news, selected papers
│   ├── research.md              # /research/  — research interests / threads
│   ├── publications.md          # /publications/ — auto-renders from papers.bib
│   ├── talks.md                 # /talks/  — invited & contributed talks
│   ├── teaching.md              # /teaching/ — teaching philosophy & mentees
│   ├── news.md                  # /news/   — press, media, public outreach
│   ├── outreach.md              # /outreach/ — outreach, mentoring, leadership, service
│   └── cv.md                    # /cv/     — markdown CV with PDF download
├── _bibliography/papers.bib     # the publication list
├── _data/cv.yml                 # optional structured CV (alternate layout)
├── _data/socials.yml            # social-icon links shown in About sidebar
├── _news/                       # short "news ticker" items shown on /
│   └── announcement_*.md
├── assets/
│   ├── img/prof_pic.jpg         # PUT YOUR HEADSHOT HERE
│   └── pdf/CV.pdf               # auto-overwritten by the Overleaf sync workflow
└── .github/workflows/
    ├── deploy.yml               # builds Jekyll, publishes to gh-pages
    └── sync-cv.yml              # nightly: pulls Overleaf, compiles, commits PDF
```

---

## one-time setup

### 1. Fork al-folio and overlay these files

al-folio is a complete Jekyll theme. The cleanest way to set this up is to
*start from a fresh clone of al-folio* and then overlay the files in this
folder.

```bash
# Clone al-folio into the repo name GitHub Pages expects.
git clone https://github.com/alshedivat/al-folio.git navinsridhar.github.io
cd navinsridhar.github.io

# Remove al-folio's history so this becomes your repo.
rm -rf .git
git init -b main

# Overlay the contents of this folder on top.
# (Either copy file-by-file in your editor, or rsync from where you saved
#  this archive — replace the path below with wherever you placed it.)
rsync -av --exclude='.git' /path/to/this/folder/  ./

# Drop your headshot in.
cp /path/to/your/headshot.jpg assets/img/prof_pic.jpg
```

### 2. Create the GitHub repo

On GitHub, create a **new public repo** named exactly **`navinsridhar.github.io`**
(no description / README — leave it empty).

```bash
git add .
git commit -m "Initial commit — al-folio personal website"
git remote add origin https://github.com/navinsridhar/navinsridhar.github.io.git
git push -u origin main
```

### 3. Enable GitHub Pages (gh-pages branch)

On GitHub: **Settings → Pages → Build and deployment**, set:

- **Source:** *Deploy from a branch*
- **Branch:** `gh-pages` / `(root)`

The first push to `main` triggers `.github/workflows/deploy.yml`, which builds
the site and pushes the compiled output to `gh-pages`. After ~1 min the site
is live at **https://navinsridhar.github.io**.

### 4. (One-time) configure the Overleaf → CV sync

The workflow at `.github/workflows/sync-cv.yml` runs **once a day at 08:00 UTC**
(also runnable on demand from the Actions tab). It clones your Overleaf CV
project, compiles it with `latexmk`, and commits `assets/pdf/CV.pdf`.

You need to give it credentials:

1. **Get your Overleaf project's git URL.** On Overleaf, open the project →
   **Menu → Sync → Git**. Copy the URL (looks like
   `https://git.overleaf.com/<project-id>`). *This requires Overleaf
   Premium/Pro or a sitewide-license institution* — Stanford has one, so you
   should already qualify with your `@stanford.edu` account.

2. **Generate an Overleaf access token.** Overleaf → click your avatar →
   **Account Settings → Git Integration → Generate token**. Copy it (you'll
   only see it once).

3. **Add both as GitHub secrets.** On the GitHub repo:
   **Settings → Secrets and variables → Actions → New repository secret**.

   | Name                 | Value                                      |
   |----------------------|--------------------------------------------|
   | `OVERLEAF_GIT_URL`   | the URL from step 1, e.g. `https://git.overleaf.com/abc123…` |
   | `OVERLEAF_GIT_TOKEN` | the token from step 2                      |

4. **(Optional) tell the workflow what your top-level .tex file is named.**
   The default is `main.tex`. If yours is named e.g. `CV.tex` or
   `Sridhar_CV.tex`, add a **repository variable** (same UI tab, "Variables"
   sub-tab) called `MAIN_TEX_FILE` with the value (e.g. `CV.tex`).

5. **Run it once manually.** Actions tab → *Sync CV from Overleaf* →
   *Run workflow*. After ~ 2 min you should see `assets/pdf/CV.pdf` updated
   on `main`.

From then on, every change you push to Overleaf will be reflected on the
website by the next morning.

---

## local development

```bash
bundle install
bundle exec jekyll serve --livereload
# open http://localhost:4000
```

If you change `_config.yml`, restart the server.

---

## customisation cheat-sheet

| What you want to change       | Where                                            |
|-------------------------------|--------------------------------------------------|
| Bio paragraph on landing page | `_pages/about.md`                                |
| Profile photo                 | `assets/img/prof_pic.jpg`                        |
| Site title / colour theme     | `_config.yml` (`title`, `theme_color`)           |
| Add/remove a navbar tab       | front-matter `nav: true / false` in `_pages/*.md` |
| Add a publication             | `_bibliography/papers.bib`                       |
| Mark a paper as "selected"    | add `selected = {true}` to its bib entry         |
| Front-page news item          | drop a new `_news/announcement_N.md`             |
| Social links in sidebar       | `_data/socials.yml`                              |
| Custom domain (e.g. `navinsridhar.com`) | put it in `cname:` in `deploy.yml` and add a `CNAME` file at the repo root |

---

## credit & licence

- Theme: **al-folio** by [Maruan Al-Shedivat](https://github.com/alshedivat/al-folio) (MIT).
- Content © Navin Sridhar.
