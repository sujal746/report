#!/usr/bin/env bash
# Run this once after you change your GitHub username.
#
#   ./site/after-rename.sh NEW_USERNAME
#
# It points the git remote at the new account, rebuilds the site (all links
# inside the page are derived from the remote), and pushes.
set -euo pipefail

NEW="${1:-}"
if [[ -z "$NEW" ]]; then
  echo "Usage: $0 NEW_USERNAME" >&2
  exit 1
fi

cd "$(dirname "$0")/.."

REPO="$(basename "$(git remote get-url origin)" .git)"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

echo "Old remote: $(git remote get-url origin)"
git remote set-url origin "https://github.com/$NEW/$REPO.git"
echo "New remote: $(git remote get-url origin)"

PY=".venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Creating build environment..."
  python3 -m venv .venv
  .venv/bin/pip install -q --disable-pip-version-check markdown
fi
"$PY" site/build.py

git add -A
git commit -m "Update site links for new GitHub account: $NEW"
git push origin "$BRANCH"

cat <<EOF

Done. Next steps:
  1. Open https://github.com/$NEW/$REPO/settings/pages and confirm the source
     is still branch "$BRANCH", folder "/docs" (re-save if it looks blank).
  2. Open https://$NEW.github.io/$REPO/ and check the site loads.
  3. GitHub redirects the old address, so links you already shared keep working.
EOF
