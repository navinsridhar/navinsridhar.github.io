# Replace SRC with the actual path to the "Navin - personal website" folder I built.
SRC="/Users/navin/Downloads/Navin - personal website"   # <-- edit this

rsync -av --exclude='.git' --exclude='.DS_Store' --exclude='assets/img/README_image.md' "$SRC"/ ./
rm -f Gemfile.lock

git add -A
git rm -f --ignore-unmatch Gemfile.lock
git commit -m "Sync latest overlay from generator"
git push
