# CONVERSATION-01 + Command Center V2 — audit des modules (14/11/2026)

Audit en lecture seule, réalisé avant toute intégration. Sources : branches de développement les plus récentes des huit dépôts. Le principe directeur : **réutiliser** ce qui existe et est testé, ne rien reconstruire.

## 1. Ce qui fonctionne réellement aujourd'hui (preuves CI)

| Capacité | Où | Preuve |
|---|---|---|
| Conversation texte locale, contexte de session (3 échanges) | V1 `labs/v1` (CORE `5da9838` + LLM A02 `2e01177`) | run 43313299256 (API 29/35) |
| Moteur LLM scellé, Qwen3-0.6B vérifié par SHA | LLM A02 | traces A02 (15 scellés, fd scellé) |
| STT whisper.cpp + Pocket TTS (voix publique alba) | V1 `:stt` / `:pocket` (VOICE `92d0745`) | aller-retour TTS→STT exact (API 29/35) |
| Cockpit V3 (sphère, fiches, menu radial) branché sur la session V1 | `labs/v3` | run 43522819722 |
| Interruption, libération mémoire, garde thermique et mémoire | V1Session | tests b/d/g V1 |

## 2. Composants existants et testés, mais NON branchés dans l'application

| Composant | Dépôt / emplacement | Utilité pour CONVERSATION-01 |
|---|---|---|
| **Identité / personnalité** : `PersonaPreset.ATHENA` (franchise 75, humour 60, initiative 100, tutoiement, style ÉLÉGANT), `PersonaParameters`, contextes DAILY/WORK/URGENT, `ContextStylePolicy`, `IdentityStyleFormatter`, `ProfileRepository` (révisions, restauration), `PersonaInterestCatalog` | CORE `5da9838` (déjà épinglé par la V1), `identity/` | Base de la personnalité structurée et persistante. **Athéna existe déjà comme préréglage.** |
| **Mémoire consentie** : `MemoryApprovalWorkflow` (Proposed→Confirmed avec reçu de consentement lié au digest), `ConfirmedMemoryStore` (SQLite isolée), `MemoryRecallIndex`, `MemoryContextAssembler` (bloc de données cité, borné), `MemoryExportService`, `UserMemoryControl` (fermé par défaut) | CORE `5da9838`, `memory/` | Mémoire durable autorisée, rappel contextuel, consultation, export |
| Historique persistant des messages, souvenirs, documents (SQLite V1/V2 préservée) | CORE `main` (`LocalDatabase`, correctif de préservation) | Reprise de conversation après fermeture |
| **Réactions vocales rapides** : `QuickReactionTiming` (1,2 s, refroidissement 20 s, jamais de promesse de délai), phrases « Je réfléchis à ta demande. » / « Je vérifie ça. » / « Je prépare ma réponse. » ; garde « pas de clip d'attente une fois la réponse prête » | VOICE `feat/voice-expressive-v3-android` (`92d0745`) | Premier retour vocal en moins de 5 s |
| **Connaissances** : `DocumentaryGateway` (autorisation, délai, refus fermés), `LocalRagService` (FTS5, rerankeur, budget de contexte, citations), `AndroidNexusStorage`, `SelectedDocumentImporter` (SAF) | NEXUS `codex/m53-readonly-preparation` | Recherche documentaire locale avec provenance |
| Outils et services : `ConsultationService`, `DocumentService`, `Guard`, `Memory`, ports Android SAF | SERVICES `feat/services-final-01` | Actions encadrées (lot ultérieur) |
| Écrans d'identité, panneau de mémoire confirmée, éditeur de persona | INTERFACE (application historique) | Modèles d'écran pour MEMORY VAULT / profils |
| Contrats ARCH-01 (`ModelBackend`, routage, synchronisation mémoire) | UNIFIED PR #26 | Compatibilité future PC, sans l'imposer |

## 3. Limites structurantes constatées

1. **Politique protégée A02 (V1-B)** : contexte 768 jetons, 1 thread, 3 échanges précédents maximum, sortie 128 jetons (plafond 256), instruction système fixe « Tu es JARVIS… brièvement » et instructions subordonnées routées. Avec ces valeurs, des réponses développées, un long contexte et une personnalité riche sont **mécaniquement impossibles**. Toute évolution se fait dans LLM : branche dédiée, justification mesurée, mêmes gardes mémoire et thermiques.
2. **Qualité du 0.6B** : 13/30 au banc français (M55-B). Le 1.7B obtient 21/30, avec 1,9 Gio de RSS (le POCO peut le porter ; la Redmi Pad SE est juste) ; il n'est pas encore qualifié sur Android. Le test du 1.7B en CI uniquement est autorisé.
3. **Coût du cockpit** : la sphère animée doublait le délai du premier texte sur émulateur. V3-FIX-01 la rend immobile hors réponse ; à confirmer par mesure.
4. **Voix sur émulateur** : silence au micro, aucune lecture au haut-parleur. Le micro réel, le haut-parleur et les délais perçus sont **à valider sur le POCO**.
5. **NEXUS sur Android** : passerelle et stockage Android existants, mais aucune intégration à la session conversationnelle ; l'index doit être alimenté par import autorisé (SAF).

## 4. Anomalies historiques à ne pas réintroduire

- `partial` conservé après une erreur TTS, d'où un affichage en double (corrigé V3-FIX-01, test de non-régression).
- `-noaudio` et puits audio de l'émulateur : la lecture ne progresse jamais (seul le délai de lecture exact est toléré dans les tests).
- Saisie de test : frappe système lente, `setText` concurrent ; ne jamais mélanger les deux.
- Libération non confirmée (`UnloadResult.UNKNOWN`) : aucune bascule de moteur (règle CORE).
- Un seul moteur lourd par processus, budget mémoire avant chargement, refus thermique SÉVÈRE.
- Risques ouverts A04 à A09 (rapport M55) : bail/broker, transitions terminales, chemins dans les erreurs, réservation mémoire globale.
- Aucun souvenir créé par une sortie de modèle ou un document (workflow de consentement CORE).

## 5. Plan d'intégration retenu (une seule application)

L'application unique est la lignée `labs/v3` (`fr.jarvis.v3`). Elle embarque déjà le moteur V1 inchangé ; on y ajoute, dans l'ordre :

1. **C1 — Persistance et reprise** : historique local et reprise après fermeture (schéma préservé de CORE ou magasin dédié migré proprement), mémoire de travail.
2. **C2 — Personnalité structurée** : profils CORE (`ATHENA` par défaut), paramètres persistants, contexte DAILY/WORK/URGENT, rendu en instructions subordonnées mesurées sur le vrai modèle, préférences confirmées via `MemoryPreferenceReader`.
3. **C3 — Mémoire consentie** : propositions, confirmation explicite, rappel cité, consultation, correction, suppression (MEMORY VAULT).
4. **C4 — Voix complète** : réaction rapide en moins de 5 s (`QuickReactionTiming`), interruption, anti-doublon, synchronisation avec la sphère ; trois délais mesurés séparément.
5. **C5 — Connaissances** : `DocumentaryGateway` / `LocalRagService` dans la conversation, provenance affichée, distinction vérifié / hypothèse / absent.
6. **C6 — Qualité du modèle** : banc conversationnel multi-tours (contexte, changement de sujet, correction, incertitude, personnalité) sur 0.6B et 1.7B en CI ; proposition argumentée, sans remplacement.
7. **Command Center V2** : écrans AI CORE, VOICE CENTER, MEMORY VAULT, NEXUS, MISSIONS, AGENTS, AUTOMATIONS, SECURITY, EVOLUTION LAB, BLUEPRINT, avatar 2D (zone dédiée, ressources autorisées uniquement), données réelles ou « démonstration ». La sphère reste immobile hors réponse.

Chaque lot : branche dédiée, tests JVM et instrumentés API 29/35, captures, rapport.
