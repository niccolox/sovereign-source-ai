#!/usr/bin/env bash
# Scan the news and rebuild /news/ in one step.
#
#   _tools/update_news.sh [--publish] [scan options...]
#
# Runs the news scanner in the svrnsrc.ai research repo, then rebuilds
# news/index.html here. Scan options (--days, --max-items, --model, --no-verify)
# pass straight through to tools/news_scan/scan.py.
#
# Without --publish it stops after the rebuild so you can review the page.
# With --publish it also:
#   - commits the new digest in the research repo (locally, not pushed),
#   - commits news/index.html on this repo's main branch and pushes it,
#   - fast-forwards dev to main if dev has nothing of its own,
#   - waits for the GitHub Pages build when the gh CLI is available.
#
# SVRNSRC_REPO overrides the research repo location (default ~/Projects/svrnsrc.ai).
set -euo pipefail

SITE="$(cd "$(dirname "$0")/.." && pwd)"
RESEARCH="${SVRNSRC_REPO:-$HOME/Projects/svrnsrc.ai}"

publish=0
scan_args=()
for arg in "$@"; do
  case "$arg" in
    --publish) publish=1 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) scan_args+=("$arg") ;;
  esac
done

[ -f "$RESEARCH/tools/news_scan/scan.py" ] || { echo "news scanner not found in $RESEARCH" >&2; exit 1; }

if [ "$publish" -eq 1 ]; then
  # Check every publish precondition before spending a scan.
  git -C "$RESEARCH" rev-parse --git-dir >/dev/null 2>&1 || { echo "--publish needs $RESEARCH to be a git repo" >&2; exit 1; }
  if ! git -C "$RESEARCH" diff --quiet --cached; then
    echo "--publish needs nothing else staged in the research repo" >&2; exit 1
  fi
  branch="$(git -C "$SITE" branch --show-current)"
  [ "$branch" = "main" ] || { echo "--publish needs the site repo on main (it is on $branch)" >&2; exit 1; }
  if ! git -C "$SITE" diff --quiet --cached; then
    echo "--publish needs nothing else staged in the site repo" >&2; exit 1
  fi
fi

echo "== Scanning (this takes a few minutes)"
python3 "$RESEARCH/tools/news_scan/scan.py" "${scan_args[@]}"

echo "== Rebuilding news/index.html"
python3 "$SITE/_tools/build_news.py" "$RESEARCH/research/news/data"

if git -C "$SITE" diff --quiet -- news/index.html; then
  echo "news/index.html is unchanged; nothing new to publish."
  exit 0
fi

if [ "$publish" -eq 0 ]; then
  echo
  echo "Rebuilt news/index.html. Review it, then publish with:"
  echo "  _tools/update_news.sh --publish   (rescans), or commit news/index.html and deploy as usual."
  exit 0
fi

today="$(date +%F)"
echo "== Committing the digest in the research repo (local only)"
git -C "$RESEARCH" add research/news
if git -C "$RESEARCH" diff --cached --quiet; then
  echo "research repo: nothing new to commit"
else
  git -C "$RESEARCH" commit -q -m "News scan $today"
  git -C "$RESEARCH" log --oneline -1
fi

echo "== Publishing the site"
git -C "$SITE" add news/index.html
git -C "$SITE" commit -q -m "Update news ($today)"
git -C "$SITE" push -q origin main
sha="$(git -C "$SITE" rev-parse --short=7 HEAD)"
echo "pushed $sha"

if git -C "$SITE" show-ref --verify --quiet refs/heads/dev &&
   git -C "$SITE" merge-base --is-ancestor dev main; then
  git -C "$SITE" branch -f dev main
  echo "dev fast-forwarded to main"
fi

if command -v gh >/dev/null 2>&1; then
  repo="$(git -C "$SITE" remote get-url origin | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"
  for _ in $(seq 1 36); do
    status="$(gh api "repos/$repo/pages/builds/latest" --jq '.status + " " + .commit[0:7]' 2>/dev/null || true)"
    case "$status" in "built $sha"|errored*) break ;; esac
    sleep 5
  done
  echo "GitHub Pages: ${status:-unknown}"
fi
