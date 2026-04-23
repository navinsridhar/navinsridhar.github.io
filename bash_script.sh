cd /Users/navin/Sites/navinsridhar.github.io
git pull --rebase origin main

# Rename JPG → jpg via a temporary name (two-step to defeat macOS case-insensitivity)
git mv assets/img/prof_pic.JPG assets/img/_tmp_prof_pic.jpg
git mv assets/img/_tmp_prof_pic.jpg assets/img/prof_pic.jpg

# While we're at it — auto-fix the Prettier formatting warnings
node --version || brew install node
npx prettier . --write

# Commit both fixes together
git add -A
git commit -m "Fix: lowercase profile-pic extension + Prettier formatting pass"
git push
