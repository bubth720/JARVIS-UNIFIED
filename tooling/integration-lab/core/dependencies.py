"""Source-derived facts with file digests. Missing data stays UNKNOWN."""
import re, xml.etree.ElementTree as ET
from pathlib import Path
from .integrity import git, sha

def inspect(root):
    root = Path(root); names = git(root, 'ls-tree', '-r', '--name-only', 'HEAD').decode().splitlines()
    facts = {k: [] for k in ['kotlin', 'jdk', 'gradle', 'agp', 'min_sdk', 'target_sdk', 'abi', 'cmake', 'ndk', 'native_dependencies', 'permissions', 'sqlite', 'licenses']}
    evidence = {}
    patterns = {
      'gradle': r'gradle-([\d.]+)-(?:bin|all)\.zip',
      'kotlin': r'(?:kotlin\([^\n]+?\)|org\.jetbrains\.kotlin[^\n]*?|kotlin)\s*(?:version|=)\s*"([\d.]+)"',
      'agp': r'(?:com\.android\.[a-z]+"\)\s*version\s*|agp\s*=\s*)"([\d.]+)"',
      'jdk': r'(?:jvmToolchain\(|JavaLanguageVersion\.of\(|jvmTarget\s*=\s*"|JavaVersion\.VERSION_)(\d+)',
      'min_sdk': r'minSdk\s*=\s*(\d+)', 'target_sdk': r'targetSdk\s*=\s*(\d+)',
      'ndk': r'ndkVersion\s*=\s*"([\d.]+)"', 'cmake': r'version\s*=\s*"(3\.22\.1)"',
      'abi': r'"(arm64-v8a|armeabi-v7a|x86_64|x86)"',
    }
    for name in names:
        if not (name.endswith(('build.gradle.kts', 'build.gradle', 'gradle-wrapper.properties', 'libs.versions.toml')) or name.endswith('src/main/AndroidManifest.xml') or Path(name).name.upper().startswith(('LICENSE', 'NOTICE'))): continue
        p = root / name
        if not p.is_file() or p.stat().st_size > 512*1024: continue
        text = p.read_text(errors='replace'); evidence[name] = sha(p)
        for key, pattern in patterns.items(): facts[key].extend(re.findall(pattern, text))
        facts['native_dependencies'].extend(re.findall(r'"([^"\n]*(?:onnxruntime|llama-android|sqlite-jdbc)[^"\n]*)"', text))
        if name.endswith('AndroidManifest.xml'):
            try:
                e = ET.fromstring(text)
                facts['permissions'].extend(x.get('{http://schemas.android.com/apk/res/android}name') for x in e.findall('uses-permission'))
            except ET.ParseError: facts['permissions'].append('UNKNOWN_INVALID_SOURCE_MANIFEST')
        if Path(name).name.upper().startswith('LICENSE'): facts['licenses'].append(name)
    facts = {k: sorted(set(v)) if v else 'UNKNOWN' for k, v in facts.items()}
    facts.update(ram_budget='UNKNOWN', lifecycle_qualification='UNKNOWN', authority='NOT_ACTIVATED',
                 sqlite_schema_compatibility='UNKNOWN', repository_license='UNKNOWN',
                 note='Dependency notices do not license the repository; source minSdk is not merged APK evidence.')
    return {'status': 'PASS', 'kind': 'STATIC', 'facts': facts, 'source_files_sha256': evidence}

def compare(left, right):
    reasons = []; unknown = []; mismatch = []
    for key in ['kotlin', 'jdk', 'gradle', 'agp', 'min_sdk', 'target_sdk', 'abi', 'cmake', 'ndk', 'native_dependencies', 'sqlite', 'ram_budget', 'repository_license', 'lifecycle_qualification', 'authority']:
        a, b = left['facts'].get(key, 'UNKNOWN'), right['facts'].get(key, 'UNKNOWN')
        if 'UNKNOWN' in (a, b) or a == 'NOT_ACTIVATED' or b == 'NOT_ACTIVATED': unknown.append(key)
        elif a != b: mismatch.append(key)
    status = 'INCOMPATIBLE' if mismatch else 'UNKNOWN' if unknown else 'COMPATIBLE'
    return {'status': status, 'scope': 'SHARED_TOOLCHAIN_NOT_RUNTIME', 'mismatches': mismatch, 'unknown': unknown,
            'independent_builds_allowed': True, 'runtime_connected': False}
