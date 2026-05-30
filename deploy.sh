#!/usr/bin/env bash
# One-command deploy: build, commit, push. Vercel auto-deploys within ~30s.
# Usage: ./deploy.sh "Added Stern Grove dates"
set -e

cd "$(dirname "$0")"

python3 build.py

if [[ -z $(git status --porcelain) ]]; then
  echo "Nothing to deploy — no changes since last build."
  exit 0
fi

MSG="${1:-Update events}"
git add -A
git commit -m "$MSG"
git push

echo ""
echo "✓ Pushed. Vercel will redeploy in ~30s."
echo "  Check status: gh repo view --web"
