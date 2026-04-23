cd /Users/navin/Sites/navinsridhar.github.io

# Check al-folio's package.json is present
ls package.json

# Install the dev dependencies it declares (Prettier + the Liquid plugin)
npm install

# Now Prettier can find the plugin
npx prettier . --write

# Commit and push
git add -A
git commit -m "Prettier formatting pass"
git push
