git pull --rebase origin main

# 1. Kill the sample Jupyter notebook (and its assets) that's causing the fatal error.
rm -rf assets/jupyter

# 2. Disable the jekyll-jupyter-notebook plugin entirely — you're not blogging
#    notebooks right now. Easy to re-enable later if you want.
python3 - <<'PY'
import pathlib, re

# Remove from _config.yml plugins list
cfg = pathlib.Path("_config.yml")
text = cfg.read_text()
text = re.sub(r"^\s*-\s*jekyll-jupyter-notebook\s*$\n?", "", text, flags=re.MULTILINE)
cfg.write_text(text)

# Remove from Gemfile
gem = pathlib.Path("Gemfile")
text = gem.read_text()
text = re.sub(r"^.*jekyll-jupyter-notebook.*$\n?", "", text, flags=re.MULTILINE)
gem.write_text(text)

print("Patched _config.yml and Gemfile.")
PY

# 3. Delete the lockfile so CI regenerates cleanly with the slimmer Gemfile.
rm -f Gemfile.lock

# 4. (Optional but recommended) delete the sample blog posts — this kills the
#    archive-layout warnings. You can add your own posts anytime.
rm -rf _posts/*

git add -A
git commit -m "Remove jekyll-jupyter-notebook + sample notebook/blog posts"
git push

