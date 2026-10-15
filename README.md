# JARVIS-UNIFIED

Préparation d'une application Android JARVIS unique, modulaire et entièrement
hors ligne. **Mission 002 : prototype fictif de sauvegarde/restauration terminé.**
Aucune application fusionnée, aucun moteur intégré ni APK UNIFIED à cette étape.

## Mission 002 — préserver les données

- [BACKUP_FORMAT.md](BACKUP_FORMAT.md) : inventaire CORE/LLM/VOICE et archive versionnée AES-GCM/scrypt.
- [RESTORE_PLAN.md](RESTORE_PLAN.md) : usage du prototype, restauration et récupération après erreur.
- [COMPATIBILITY.md](COMPATIBILITY.md) : moteurs, profils et futur transfert Android/mini-PC.
- [MISSION_002_REPORT.md](MISSION_002_REPORT.md) : preuves, résultats et limites.
- [Prototype](backup_prototype/README.md) et [ressources](resources/README.md) : données fictives et métadonnées uniquement.

Depuis ce checkout, avec Python 3.12 et cryptography 50.0.0 :

```sh
python3 -m unittest discover -s backup_prototype/tests -v
python3 -m backup_prototype.demo
```

30 tests passent : intégrité, mémoire autorisée, conflits, erreurs IO et
récupération après interruption. Le prototype n'est pas destiné aux données réelles
ni aux poids volumineux. Aucun téléchargement automatique ou secret dans Git.
Les profils vocaux fictifs ne produisent aucun son.

## Mission 001 — audit préservé

Les cinq documents sont conservés sur `audit/mission-001` dans le commit `004b89d`.
Mission002 se trouve sur la branche `mission-002-backup`, sans fusion dans main.

- [AUDIT.md](AUDIT.md) : branches/SHAs, fonctions, preuves et limites.
- [ARCHITECTURE.md](ARCHITECTURE.md) : CORE/LLM/VOICE, contrats et mémoire confirmée.
- [MIGRATION_PLAN.md](MIGRATION_PLAN.md) : missions proposées et retours arrière.
- [TEST_PLAN.md](TEST_PLAN.md) : vérifications Mission001 et qualification future.

CORE reprendrait orchestration, mémoire, documents et Whisper de
[bubth720/JAVIS-Local-v2](https://github.com/bubth720/JAVIS-Local-v2).
LLM reprendrait le moteur unique et les protections de
[bubth720/JARVIS-LLM](https://github.com/bubth720/JARVIS-LLM), branche 003B.
VOICE préparerait la synthèse neuronale et les profils personnels de
[bubth720/JARVIS-VOICE](https://github.com/bubth720/JARVIS-VOICE), branche Android
005D/E/F/G. Aucun TTS Android générique ne remplace la voix personnalisée.
La ressemblance personnelle et le naturel restent à qualifier sur appareil.

Références initiales évolutives : TABLET Redmi Pad SE / Qwen3 0,6B Q4_K_M ;
MOBILE POCO X8 Pro / Qwen3 1,7B Q4_K_M ; CENTRAL mini-PC/modèles à qualifier.
Aucun des trois dépôts sources n'a été modifié ou supprimé. Aucune dépendance
cloud obligatoire. Aucune mission suivante n'est commencée.

Travailler dans le checkout existant, sans worktree supplémentaire. Les données,
audios, profils personnels et clés restent hors Git et hors du présent prototype.
