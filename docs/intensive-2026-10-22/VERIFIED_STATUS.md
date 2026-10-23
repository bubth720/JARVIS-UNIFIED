# Campagne JARVIS — état local vérifié

Prêtes : aucune

Livrées avec preuves vérifiables : AVA-01, CORE-01, CORE-02, EVOL-01, EVOL-02, ID-01, LLM-01, MEM-01, NEX-01, NEX-02, NEX-03, NEX-05, SERV-01, SERV-02, SERV-03, UNI-01, UNI-02, VOICE-01

| Mission | État | Blocage |
|---|---|---|
| CORE-01 | DELIVERED |  |
| CORE-02 | DELIVERED |  |
| CORE-03 | PREPARED | Repository already owned |
| ID-01 | DELIVERED |  |
| ID-02 | IN_PROGRESS |  |
| MEM-01 | DELIVERED |  |
| MEM-02 | PREPARED | Repository already owned |
| LLM-01 | DELIVERED |  |
| LLM-02 | BLOCKED | Incrément logiciel publié ; tokenisation exacte/worker natif non qualifiés. |
| LLM-03 | BLOCKED | Dependency not delivered: LLM-02; Incrément logiciel publié ; tokenisation exacte/worker natif non qualifiés. |
| VOICE-01 | DELIVERED |  |
| VOICE-02 | BLOCKED | Incrément publié 3ffb28011506abcc94b5d4ee71d6c79fc278333b ; modulation native et rendu physique non qualifiés. |
| VOICE-03 | PREPARED | Dependency not delivered: VOICE-02 |
| UI-01 | BLOCKED | Incrément UI publié 48db1ecbb40dfa5b90a8e696fe6c2a62228f5ce9 ; CORE02 ne fournit pas de contenu/soumission externe, aucun transport activé.; Repository already owned |
| UI-02 | IN_PROGRESS |  |
| AVA-01 | DELIVERED |  |
| AVA-02 | PREPARED | Dependency not delivered: VOICE-02; Repository already owned |
| SERV-01 | DELIVERED |  |
| SERV-02 | DELIVERED |  |
| SERV-03 | DELIVERED |  |
| NEX-01 | DELIVERED |  |
| NEX-02 | DELIVERED |  |
| NEX-03 | DELIVERED |  |
| NEX-04 | IN_PROGRESS |  |
| NEX-05 | DELIVERED |  |
| EVOL-01 | DELIVERED |  |
| EVOL-02 | DELIVERED |  |
| EVOL-03 | BLOCKED | Tranche inerte publiée c0180181804338d21f3bf9d4b537b709595902f7 ; sandbox OS non qualifiée : bwrap uid map read-only. |
| EVOL-04 | BLOCKED | Dependency not delivered: EVOL-03; EVOL-03 ne fournit pas de runner OS qualifié. |
| UNI-01 | DELIVERED |  |
| UNI-02 | DELIVERED |  |

## Décisions manuelles conservées

- LLM-02 : Aucune activation JNI/F3B ou réconciliation CORE004D autorisée.
- LLM-03 : Aucune activation JNI/F3B ou réconciliation CORE004D autorisée.
- UI-01 : NON CONNECTÉ par défaut ; démo explicitement sans CORE/LLM.
- EVOL-03 : Aucun patch non fiable exécuté, aucune nouvelle tentative de contournement.
- VOICE-02 : Timeline de segments/pauses PCM logicielle disponible ; aucun phonème ni clock playback attesté.

Les vagues sont un plan ; elles ne prouvent aucune intégration native ou physique.
