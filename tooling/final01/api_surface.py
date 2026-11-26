"""F01 — public Kotlin/Java API surface of a module at an exact commit, and its diff between two commits.

Read-only: uses `git show` on the given SHAs, never checks out or edits. A declaration is public unless marked
private/internal/protected (Kotlin default visibility is public). Signatures are normalised (whitespace, comments,
default values kept) so a renamed parameter, a changed type or a removed member is reported. The comparison answers
"did the producer change its contract?" — it does not judge whether a change is compatible; any removal or change is
BREAKING_CANDIDATE and must go through a major version and an explicit migration (FINAL-01 F01).
"""
import argparse, json, re, subprocess, sys

DECL = re.compile(r'^\s*((?:(?:public|open|abstract|sealed|data|enum|value|inline|suspend|override|operator|infix|'
                  r'tailrec|external|const|lateinit|final|annotation|fun|companion|inner)\s+)*)'
                  r'(class|interface|object|fun|val|var|typealias|enum class)\b(.*)$')
HIDDEN = re.compile(r'\b(private|internal|protected)\b')

def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], check=True, capture_output=True, text=True).stdout

def strip_comments(src):
    src = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), src, flags=re.S)
    return re.sub(r'//[^\n]*', '', src)

def cut_body(sig):
    """Signature without its body: stops at the first '=' or '{' outside parentheses/angle brackets."""
    depth = 0
    for i, c in enumerate(sig):
        if c in '(<': depth += 1
        elif c == ')' or (c == '>' and sig[i - 1:i] != '-'): depth -= 1
        elif c in '={' and depth == 0: return sig[:i].strip()
    return sig.strip()

def declarations(path, src):
    """Top-level and member declarations that are not hidden, with their package-qualified owner path."""
    out, package, depth, owners = [], '', 0, []
    for line in strip_comments(src).split('\n'):
        p = re.match(r'\s*package\s+([\w.]+)', line)
        if p: package = p.group(1)
        m = DECL.match(line)
        if m and not HIDDEN.search(line.split(m.group(2))[0]) and (not owners or owners[-1][1]):
            sig = cut_body(' '.join((m.group(1) + m.group(2) + m.group(3)).split()))
            owner = '.'.join([package] + [o[0] for o in owners])
            out.append(f'{owner} :: {sig}')
        opened, closed = line.count('{'), line.count('}')
        if m and m.group(2) in ('class', 'interface', 'object', 'enum class') and opened > closed:
            name = re.match(r'\s*([\w]+)', m.group(3)); visible = not HIDDEN.search(line.split(m.group(2))[0])
            owners.append((name.group(1) if name else '?', visible and (not owners or owners[-1][1]), depth))
        depth += opened - closed
        while owners and depth <= owners[-1][2]: owners.pop()
    return out

def surface(repo, sha, roots):
    files = [f for f in git(repo, 'ls-tree', '-r', '--name-only', sha, '--', *roots).split('\n') if f.endswith(('.kt', '.java'))]
    api = {}
    for f in files:
        if '/test/' in f or '/androidTest/' in f: continue
        for d in declarations(f, git(repo, 'show', f'{sha}:{f}')): api.setdefault(d, f)
    return api

def compare(repo, base, head, roots):
    a, b = surface(repo, base, roots), surface(repo, head, roots)
    removed = sorted(set(a) - set(b)); added = sorted(set(b) - set(a))
    status = 'IDENTICAL' if not removed and not added else ('ADDITIVE' if not removed else 'BREAKING_CANDIDATE')
    return {'repo': repo, 'base': base, 'head': head, 'roots': roots, 'status': status,
            'public_declarations_base': len(a), 'public_declarations_head': len(b), 'removed_or_changed': removed, 'added': added}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo'); ap.add_argument('base'); ap.add_argument('head'); ap.add_argument('roots', nargs='+')
    r = compare(**vars(ap.parse_args()))
    json.dump(r, sys.stdout, indent=1, ensure_ascii=False); print()
    sys.exit(0 if r['status'] != 'BREAKING_CANDIDATE' else 3)
