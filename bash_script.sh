# Install Node if you don't have it yet.
node --version || brew install node

# Auto-format everything.
npx prettier . --write

# Commit the formatting pass.
git add -A
git commit -m "Run Prettier over the site"
git push
