#!/usr/bin/env bash
# F00 — reproducible GitHub collection (read-only). Output in $1. CORE (JAVIS-Local-v2) PR titles/states come from
# the search API and PR heads from `git ls-remote` (its REST API is not enabled for the collecting session).
set -euo pipefail; D="$1"; mkdir -p "$D"; cd "$D"; : > prs.jsonl; : > branches.jsonl
for r in JARVIS-LLM JARVIS-VOICE JARVIS-INTERFACE JARVIS-NEXUS JARVIS-VOLUTION- JARVIS-SERVICES JARVIS-UNIFIED; do
  gh api --paginate "repos/bubth720/$r/pulls?state=all&per_page=100" --jq '.[] | {repo:"'$r'", number, title, state, draft, merged_at, created_at, updated_at, head_ref:.head.ref, head_sha:.head.sha, base_ref:.base.ref, base_sha:.base.sha, labels:[.labels[].name], url:.html_url}' >> prs.jsonl
  gh api --paginate "repos/bubth720/$r/branches?per_page=100" --jq '.[] | {repo:"'$r'", name, sha:.commit.sha, protected}' >> branches.jsonl
done
git ls-remote https://github.com/bubth720/JAVIS-Local-v2 > lsremote-core.txt
gh api -X GET search/issues -f q='repo:bubth720/JAVIS-Local-v2 is:pr' -f per_page=100 > search-core.json
echo "then: CI per head (commits/<sha>/check-runs), pulls/<n> mergeable_state, and tools/analyse_prs.py on local clones with refs/pull/*/head fetched"
