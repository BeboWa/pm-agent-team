#!/usr/bin/env bash
# Shows, in plain English, what is on GitHub and what is not.
# Usage (from anywhere inside the project):  bash scripts/check_push_status.sh
set -u
cd "$(git rev-parse --show-toplevel)" || { echo "Not inside a git project."; exit 1; }
branch=$(git rev-parse --abbrev-ref HEAD)
up="origin/$branch"
echo "Project: $(basename "$PWD")   Branch: $branch"
if git fetch origin --quiet 2>/dev/null; then echo "(checked GitHub just now)"; else echo "(could not reach GitHub; results may be out of date)"; fi

echo; echo "1) Saved locally (committed) but NOT pushed to GitHub:"
unpushed=$(git log --oneline "$up"..HEAD 2>/dev/null)
if [ -n "$unpushed" ]; then echo "$unpushed" | sed 's/^/   /'; else echo "   none"; fi

echo; echo "2) Changed or new files NOT yet committed:"
dirty=$(git status --short)
if [ -n "$dirty" ]; then echo "$dirty" | sed 's/^/   /'; else echo "   none"; fi

echo; echo "3) On GitHub but not on this computer:"
behind=$(git log --oneline HEAD.."$up" 2>/dev/null)
if [ -n "$behind" ]; then echo "$behind" | sed 's/^/   /'; else echo "   none"; fi

echo; echo "4) Key parts of the project, as they appear on GitHub:"
for path in agents/diagnostic agents/pricing_billing agents/discovery agents/prioritization agents/prd agents/delivery \
            agents/launch agents/analytics agents/reviewer agents/brief agents/deliverables agents/orchestrator \
            intake tests shared/paths.py .github/workflows/tests.yml README.md; do
  if [ -n "$(git ls-tree -r --name-only "$up" -- "$path" 2>/dev/null | head -1)" ]; then
    printf "   on GitHub      %s\n" "$path"
  elif [ -e "$path" ]; then
    printf "   NOT on GitHub  %s   (it exists on your computer)\n" "$path"
  else
    printf "   missing        %s   (not on your computer either)\n" "$path"
  fi
done

echo
if [ -z "$unpushed" ] && [ -z "$dirty" ]; then echo "Summary: everything on this computer is on GitHub."
else echo "Summary: some work is not on GitHub yet. To push it:  git add -A && git commit -m \"your message\" && git push"; fi
