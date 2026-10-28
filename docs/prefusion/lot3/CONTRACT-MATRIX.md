# Lot3 — matrice candidate, non autorisée en production

Référence de coordination : e4c678faf630a0a98adfaecd7a87fc11dfd82486.
Les contrats UNIFIED v1/v2 et leurs locks restent intacts. Les DTO de laboratoire
ne sont pas déclarés équivalents aux contrats approuvés ni aux endpoints réels.

| Producteur → consommateur | Contrat et preuve consommateur | SDK / identité / permissions | Autorité et gate |
|---|---|---|---|
| CORE → INTERFACE | Port metadata `jarvis.core-ui.readonly-lab/1-draft`; tests CORE de corrélation/refus et UI fixtures locales, pas E2E entre APK | CORE24/UI26; UID et certificat doivent venir du transport Android, jamais du payload; aucun service/permis ajouté | CORE décide; LAB reste UNTRUSTED/OFF. Signature réelle BLOCKED |
| CORE → NEXUS | Adaptateurs documentaires existants; diagnostic lot3 FTS et SAF, recherche RAG non démontrée = UNSUPPORTED | API24/25 à qualifier; URI choisie + consentement + droit de lecture révocable; provider synthétique isolé uniquement | CORE autorise l'accès, NEXUS possède l'index; aucune migration/backend natif activé |
| CORE → SERVICES | Banc déterministe de reçu, Preview, token unique, génération/commit; tests consommateurs de refus | API24; identité injectée dans test ne prouve aucun appelant Android; aucun export SAF production | Autorité CORE unique; journal/durable readback et mapping d'états BLOCKED avant ADR-002 |
| CORE → LLM | Fixture /2 et observations F3 historiques; stop demandé ≠ calcul fini ≠ unload attesté | Compatibilité SDK et contrat exact à négocier; aucune nouvelle permission | Un seul lourd; preuve JNI/unload et réconciliation restent BLOCKED |
| CORE → VOICE | Contrats pilote historiques, packs spécifiques au moteur | SDK/certificats à qualifier; aucune voix privée ou pack déplacé | CORE orchestre, VOICE possède son moteur; libération native non qualifiée = BLOCKED |

La projection Python `prefusion_lot3.py` est un vérificateur de transcription
**synthétique**; elle ne consomme pas les classes Kotlin des propriétaires.
Le parcours TXT/CSV conserve le digest et les identifiants, puis NEXUS UNSUPPORTED
est affiché comme UNAVAILABLE. Aucune citation ou réponse documentaire inventée.

## Lecture des preuves

JVM = comportement du code sous hôte. Robolectric = simulation Android.
Compilation d'androidTest ≠ exécution sur émulateur. CI verte d'un SHA antérieur
ne vaut pas pour un nouveau SHA. Une signature RSA de fixture n'atteste pas l'UID
Android. Aucun de ces résultats ne constitue une qualification physique.

## Écarts vérifiés du port CORE

Le draft metadata CORE n'est pas le wire UI03. Son epoch locale n'est pas l'epoch
signée du bus existant. Il refuse un bus multi-requêtes ou une séquence initiale
incompatible : pas de conversion silencieuse ni promesse de routage runtime.
Les références diagnostiques NEXUS201f0d/SERVICESea541 ne remplacent pas les
bibliothèques réellement consommées par integration-lab (NEXUS777e/SERVICES3de).
Un changement de dépendance attend une mission et une validation séparées.
