"""Versioned commands, never shell fragments from module metadata."""
from pathlib import Path
from tooling.integration.lock import REPOSITORIES

MODULES = {k.upper(): v for k, v in REPOSITORIES.items()}
STATUSES = {'PASS', 'FAIL', 'BLOCKED', 'NOT_RUN', 'UNKNOWN', 'PARTIAL'}
KINDS = {'UNIT', 'INTEGRATION', 'NATIVE', 'EMULATOR', 'PHYSICAL', 'STATIC', 'SIMULATION'}
EXIT = {'PASS': 0, 'FAIL': 2, 'INCOMPATIBLE': 3, 'BLOCKED': 4, 'UNKNOWN': 5, 'PARTIAL': 6, 'NOT_RUN': 4}

# argv, evidence kind, timeout seconds. No model acquisitions, native patching or runtime grants.
PYTHON = {
 'core-scope': ('CORE', ['-m', 'unittest', 'discover', '-s', 'tests/m50_s1', '-v'], 'UNIT', 120),
 'llm-perf02': ('LLM', ['-m', 'unittest', 'discover', '-s', 'perf02', '-p', 'test_*.py', '-v'], 'UNIT', 120),
 'llm-historical-guard': ('LLM', ['tools/check-prefusion.py'], 'STATIC', 60),
 'llm-manifest-guard': ('LLM', ['tools/check-preservation-003e.py'], 'STATIC', 60),
 'interface-host': ('INTERFACE', ['-m', 'unittest', 'discover', '-s', 'm51', '-p', 'test_*.py', '-v'], 'UNIT', 120),
 'nexus-sqlite': ('NEXUS', ['-m', 'unittest', 'discover', '-s', 'tests/final', '-v'], 'INTEGRATION', 120),
 'unified-validator': ('UNIFIED', ['scripts/validate_unified.py'], 'STATIC', 120),
 'unified-tests': ('UNIFIED', ['-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'UNIT', 180),
 'unified-registry': ('UNIFIED', ['-m', 'unittest', 'discover', '-s', 'registry/tests', '-v'], 'UNIT', 120),
 'unified-backup': ('UNIFIED', ['-m', 'unittest', 'discover', '-s', 'backup_prototype/tests', '-v'], 'UNIT', 120),
 'unified-campaign': ('UNIFIED', ['-m', 'unittest', 'discover', '-s', 'tooling/campaign/tests', '-v'], 'UNIT', 120),
 'unified-integration': ('UNIFIED', ['-m', 'unittest', 'discover', '-s', 'tooling/integration/tests', '-v'], 'UNIT', 120),
 'unified-v1': ('UNIFIED', ['-m', 'unittest', 'discover', '-s', 'tooling/v1/tests', '-v'], 'UNIT', 120),
}
GRADLE = {
 'nexus-jvm': ('NEXUS', ['-I', 'm53review/init.gradle', ':nexus-core:test', ':nexus-jvm-store:test', ':nexus-cli:assemble'], 'UNIT', 900, '8.10.2'),
 'voice-jvm': ('VOICE', [':expressionRuntime:test', ':voiceBridgeContract:test', ':voiceFinalSdk:test'], 'UNIT', 900, '8.13'),
 'services-jvm': ('SERVICES', [':desktop:test'], 'UNIT', 900, '8.13'),
 'evolution-jvm': ('EVOLUTION', ['test', ':evolution-cli:installDist'], 'UNIT', 900, '8.13'),
 'interface-m51': ('INTERFACE', ['-I', 'm51/lab.init.gradle', '-Pm51R1=true', ':app:testDebugUnitTest', ':m51lab:testBaselineDebugUnitTest', ':m51lab:testCandidateDebugUnitTest', ':m51lab:assembleBaselineDebug', ':m51lab:assembleCandidateDebug', ':m51lab:assembleBaselineDebugAndroidTest', ':m51lab:assembleCandidateDebugAndroidTest', ':m51lab:lintCandidateDebug'], 'UNIT', 1200, '8.13'),
}
TEST_IDS = list(PYTHON) + ['llm-native-helpers', 'voice-jvm', 'services-jvm', 'evolution-jvm']
BUILD_IDS = ['nexus-jvm', 'interface-m51']

def command_owner(identifier):
    if identifier in PYTHON: return PYTHON[identifier][0]
    if identifier in GRADLE: return GRADLE[identifier][0]
    if identifier == 'llm-native-helpers': return 'LLM'
    raise ValueError('UNAPPROVED_COMMAND')

def runtime_selection(names):
    if set(names) != {'INTERFACE_LOCAL_ONLY'}:
        raise ValueError('SENSITIVE_OR_UNKNOWN_RUNTIME_REFUSED')
    return ['INTERFACE_LOCAL_ONLY']

def aggregate(statuses):
    for state in ['FAIL', 'BLOCKED', 'UNKNOWN', 'PARTIAL']:
        if state in statuses: return state
    return 'PASS' if statuses and all(s == 'PASS' for s in statuses) else 'NOT_RUN'

def child(parent, name):
    p = Path(parent).resolve() / name
    if not p.resolve().is_relative_to(Path(parent).resolve()) or p.is_symlink():
        raise ValueError('UNSAFE_PATH')
    return p
