# FUSION-01 — composition candidate, non intégrée

Observation : 2026-10-25T16:54:54Z. Contrôle documentaire, jamais autorisation runtime.

| Module | SHA sélectionné | CI exacte | android24 | android25 | android26 | android29 ARM64 | Linux |
|---|---|---|---|---|---|---|---|
| core | aea5ac859ac551d54fe16187c1883a487dbee9d6 | unknown | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED | NOT_TESTED |
| evolution | c0180181804338d21f3bf9d4b537b709595902f7 | success | BLOCKED | BLOCKED | BLOCKED | BLOCKED | SUPPORTED |
| interface | db459ba388a3fea992d80320c3989be0edda8500 | success | BLOCKED | BLOCKED | NOT_TESTED | NOT_TESTED | NOT_TESTED |
| llm | 2efb3f7aa6205062ab71f570212019fd1d9885b6 | unknown | BLOCKED | BLOCKED | BLOCKED | NOT_TESTED | NOT_TESTED |
| nexus | 374ea2e2fd640e78f2f5e12e60e75b493420e504 | failure | BLOCKED | BLOCKED | BLOCKED | BLOCKED | SUPPORTED |
| services | f00091a639612b91eca1a301580c8f531249f1e3 | failure | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED | SUPPORTED |
| unified | 329f304115c9bc5b6dd6ccc2d68d19bf455b5e6c | unknown | BLOCKED | BLOCKED | BLOCKED | BLOCKED | SUPPORTED |
| voice | fe57452fcb33f5b6870070f30ba6c5f1d349c4ba | unknown | BLOCKED | BLOCKED | NOT_TESTED | NOT_TESTED | NOT_TESTED |

SUPPORTED décrit seulement la surface logicielle indiquée dans le verrou, pas un appareil qualifié.

| Phase | État | Dépendances non vérifiées | Blocages |
|---|---|---|---|
| F0 | VERIFIED |  |  |
| F1 | PARTIAL |  | Candidate API24 ports not consumed by CORE03 lab; current-session F1 not executed. |
| F3 | BLOCKED |  | Native F3B/tokenizer/unload evidence and separate sensitive authorization missing. |
| F4 | BLOCKED |  | Real correlated CORE content transport, identity and ToolApproval/Citation mapping missing. |
| F7 | PARTIAL |  | Sanitized technical observation contract not yet implemented across modules; patch runner sandbox unqualified. |
| F2 | BLOCKED | F1 | FTS5 Android unavailable/unqualified; both selected adapter CIs failed; no approved instrumented API24/25 path. |
| F5 | BLOCKED | F3, F4 | Voice admission, authenticated activation, playback clock and physical avatar qualification missing. |
| F6 | BLOCKED | F1 | NEXUS schema4/Android port divergence; SERVICES final tools not ported with full consent. |
| F8 | BLOCKED | F2, F3, F4, F5, F6, F7 | No complete Android E2E, physical validation, license clearance or production readiness. |

## Conflits à porter, sans fusion automatique

- jvm-pins-vs-api24 (F1, F2, F6, F8) : CORE03 pins NEX777/SERV3de; candidate uses NEX374/SERVf000. Source hashes and JDBC module layout differ. Action : Port the separate CORE JVM lab on a CORE-owned branch, preserve old pins/results and rerun complete F1.
- nexus-v3-v4 (F2, F6, F8) : Final d903 is schema4/JDBC and divergent from API24 schema3; ArchiveReader contracts differ. Action : Propose versioned shared schema/reader port, migration on synthetic copies only; no automatic merge.
- services-17-vs-port (F6, F8) : Final d16 contains seventeen tools, while selected API24 port exposes search/CSV with DOCX disabled. Action : Port audited tools individually through shared permissions and exact-consent gate; do not substitute the min26 APK.
- native-llm-unknown (F3, F5, F8) : Exact tokenization, stop and unload remain unqualified; CORE mapping rejects nonempty document sources/context. Action : Review native diff and provenance-preserving prompt contract separately; leave UNSUPPORTED and CORE004D blocked.
- core-voice-divergent (F5, F8) : CORE voice branch diverges and modifies AppGraph/MainActivity. Action : Review explicit port before any sensitive activation; retain historical TTS.
- voice-parallel-contracts (F5, F8) : Voice07 is parallel to final Studio; final playback events lack chat correlation and an attested clock. Action : Propose a versioned mapping, distinguish PCM buffering from playback and keep unsupported emotions.
- ui-laboratory-only (F4, F8) : UI content proposal is laboratory-only and lacks complete ToolApproval/Citation bodies and authenticated real CORE transport. Action : Keep NON CONNECTE; review transport, payloads, authentication and revocation before activation.
- distribution-licenses (F8) : Project licenses not identified; dependency licenses are not a redistribution authorization. Action : Record project and asset licenses before a distributable composed build.
