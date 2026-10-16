# Risques et portes de sécurité

| Risque | Constat / portée | Protection et preuve attendue |
|---|---|---|
| Double moteur/résidence | CORE wrapper et APK LLM existent séparément | Adaptateur unique, arbitre de portée explicite, arrêt/libération native testés |
| Perte SQLite | Ancien défaut corrigé V1→V2, migrations futures risquées | Conserver correctifs/fixtures, sauvegarde cohérente et rollback avant import |
| Faux consentement | /remember écrit directement dans CORE actuel | Proposer/afficher/confirmer contenu exact, transaction idempotente ; legacy inactif sans preuve |
| Régression voix | Packs/profils stricts,005D échec connu,005I styles limités | Ne pas remplacer par TTS générique ; conserver profil/pack et écoute humaine distincte des tests |
| Archives incompatibles | JVBK fictif ≠ JVIENC01 vocal | Pas de restauration/interopérabilité réelle annoncée sans adaptateur et preuve |
| Secret ou donnée personnelle | Git/log/artefact sont persistants | Rejet champs inattendus/empreintes de jetons avant écriture ; sources synthétiques, pas de logs de texte/audio |
| Batterie/chauffe/LMK | Cloud ne mesure pas Android, seuils non alloués | Capteurs valides, réserve/budgets conservés, refus, essais matériels prudents |
| IPC Android non sécurisé | Aucun pont actuel, exported/identité à concevoir | Services fermés par défaut, UID/certificat/permissions, quotas et morts de processus testés |
| Anciennes API | CORE24 vs LLM29 vs VOICE/UI26 | Matrice explicite, aucune hausse/suppression de support sans décision et test |
| GitHub requis au runtime | Risque de coupler le registre à l’app | GitHub développement seulement ; contrats/poids/profils locaux hors ligne |
| 403 GitHub | API tunnel403, écriture précédente refusée | Ne pas réessayer risqué ; paramètres réseau pour API, authentification/permissions d’écriture séparées |
| Preuve périmée/CI mal interprétée | Branches mouvantes, rapports anciens | SHA/dates/type/portée et ref_change ; absence de CI inconnue, pas verte |
| Alias/doublon mal attribué | INTERFACE-/VOLUTION-/CORE candidat | Noms exacts, relations inconnues/plausibles ; aucune suppression ou renommage |

Ces contrôles réduisent les risques ; ils ne constituent ni audit cryptographique
indépendant, ni preuve de ressemblance vocale, ni protection absolue contre root,
attaquant du même compte ou panne physique de stockage. La validation applicative
et matérielle reste dans les missions autorisées des propriétaires de runtime.

## Sévérité de clôture 001F

- **Critique avant migration :** perte de données/voix, changement de signature ou
  double résidence de modèles. Bloquer transfert/désinstallation sans sauvegarde,
  restauration et qualification. Aucun de ces changements n’est effectué ici.
- **Élevée avant IPC :** client usurpé, autorisation textuelle, réponse tardive,
  mort native non confirmée, contrôle interprocessus absent ; tester UID/certificat,
  refus fermé, sessions/générations, arrêt effectif avant admission suivante.
- **Élevée appareil :** RAM/LMK, thermique et batterie non mesurés ici, API24/29
  incompatibles ; conserver protections et refuser essais non admissibles.
- **Élevée gouvernance :** publication403 et preuves CI inaccessibles ; bundle
  vérifié et rapport distinguent local/distant. Ne pas appeler un rapport CI vert
  une observation Actions de cette mission.
- **Modérée maintenance :** multiples APK/contrats fermés/noms ambigus/snapshots
  périmés ; ADR toujours proposée, fraîcheur et mises à jour après PR approuvée.

Aucun nouveau résultat ne valide clonage, expression acoustique, migration privée
H→I, avatar rendu ou parcours inter-applications. Préserver les échecs historiques.
