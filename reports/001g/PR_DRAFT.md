# Consolidation JARVIS : registre, sauvegarde, ADR-001 approuvée et maintenance001G

UNIFIED centralise désormais l’inventaire sourcé des neuf dépôts, les preuves,
contrats proposés, sauvegarde fictive et feuille de route. La chaîne de commits
préserve les missions001/002/003/001F, la décision utilisateur ADR-001 et le correctif
001G ; aucune application externe n’est modifiée.

ADR-001 option3 **approuvée avec précisions le15 octobre2026**, exclusivement
l’orientation : CORE orchestrateur et adaptateurs interchangeables. Transport,
signatures, nombre d’APK, arbitre, migrations et performance restent à décider.
Aucun raccordement ou déploiement autorisé par cette PR.

001G corrige uniquement l’attente obsolète15→16 dans test_read_valid_registry :
les15 missions d’origine sont inchangées et UNIFIED-001F est une addition légitime.
Aucune donnée modifiée ni test désactivé. Ancien échec conservé en preuve.

Validation locale : **80/80 réussis, aucun échec ni saut** (27 audit/contrats,
23 registre,30 sauvegarde), validate_unified et registre --validate-only réussis.
Voir MISSION_001G_REPORT.md et reports/001g/validation.json pour commandes/logs.
Ces résultats ne valent ni CI GitHub observée ni essai Android/appareil.
Aucun lien runtime CORE↔LLM/VOICE démontré ou développé.

Sept branches publiées sans forçage, SHA vérifiés ; main e4435f4 inchangée.
Sauvegarde Git complète et restauration isolée vérifiées. Risques : les contrats
et migrations restent à spécifier/qualifier, les sauvegardes applicatives sont
fictives. Conserver l’historique des rapports et la portée des preuves.

**PR BROUILLON uniquement : ne pas fusionner, ne pas activer l’auto-merge.**
