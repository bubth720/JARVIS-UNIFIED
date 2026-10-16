# Contrats v1 — proposés, sans transport implémenté

Version : protocole 1.0, contrats 1.0.0. Les cinq schémas draft2020-12 sont des
interfaces portables **proposées**, pas des preuves de liaison entre APK. Les
exemples sont synthétiques ; `available:false` et les réponses MODULE_ABSENT
n'activent aucun moteur. Aucun HTTP, URL cloud, chemin privé ou prompt dans les
métadonnées. Les payloads sont des références privées opaques à résoudre dans un
adaptateur local autorisé, pas des chemins de fichiers choisis par un LLM.

## Portée des cinq contrats

- capability-manifest : module/version, capacités, environnement, compatibilités
  exactes moteur/modèle/profil. L'annonce n'autorise pas son appel. `unknown`
  interdit de supposer disponible. Pas de profil vocal universel.
- request-envelope : corrélation, origine/destination/capacité, session et référence
  d'autorisation, limites, délai et identifiant d'annulation. text.generate exige
  le digest du modèle ; speech.synthesize exige profil et pack précis.
- response-envelope : même corrélation et bon module émetteur ; résultat OU erreur,
  jamais succès avec erreur. Provenance bornée sans prompt/URI/clé ; résultat en
  objet privé référencé. Généré n'est pas lu/audible ; aucun compteur de temps
  ne vaut preuve perceptive. Les erreurs couvrent absence, incompatibilité,
  non-autorisation, interruption, expiration, annulation, ressources et nettoyage.
- resource-lease : propriété coopérative, classe lourd/résidence et génération.
  Stop demandé ≠ fin native ≠ libération. `released` exige effective_end vrai,
  release_confirmed vrai et aucune résidence. cleanup_failed reste bloquant.
  Aucun bail ne réserve directement la RAM Android ; le coordinateur LLM actuel
  ne couvre que son processus, pas CORE/VOICE ou un futur PC.
- health-status : disponible/indisponible/dégradé/inconnu, codes fermés, diagnostics
  minimaux nullable. `unknown` n'est jamais OK ; aucun contenu ni chemin privé.

`limits` n'augmente aucune permission ni aucun budget : l'adaptateur retient le
minimum entre la demande et la politique matérielle qualifiée. Le rôle déclaré
`origin` et authorization_ref ne prouvent pas une identité : Binder UID, certificat
et permission de signature doivent être contrôlés par le futur transport.
Services non exportés par défaut ; tout export requiert authentification, liste
explicite de clients, quotas et refus fermé. Le contrat n'impose ni application
unique, ni monorepo, ni mécanisme de découverte réseau.

## Temps, annulation et résidence

Les horloges monotones ne sont comparables que dans leur domaine. sent_at_ms et
expires_at_ms appartiennent à l'émetteur ; différence positive ≤ timeout_ms.
Le transport transmet un délai restant borné et construit une deadline locale
chez le destinataire. Un budget épuisé ne déclenche pas d'opération. Une réponse
à une ancienne session/corrélation est ignorée, pas rejouée sur la suivante.
Annulation idempotente ; redémarrage, heartbeat expiré ou déconnexion ne prouvent
pas la fin native. Aucun second travail lourd/résidence admis avant confirmation
de destruction ou diagnostic explicite. Une génération de bail périmée n'autorise
ni déchargement ni réutilisation du bail courant. L'arbitre interprocessus reste
à développer ; aucun test d'ici ne simule sa disponibilité réelle.

## Données et compatibilité

CORE conserve session, historique et souvenirs distincts. Une génération ou un
PDF ne peut pas confirmer un souvenir. Proposition → aperçu du contenu exact →
confirmation explicite → transaction ; legacy sans preuve reste inactif. Les
backups Mission002 restent des fixtures, pas un export Android. Préserver SQLite
V1/V2, index/citations, profils et données avant toute migration autorisée.
Le format JVBK fictif et l'archive vocale réelle JVIENC01 sont distincts ; aucune
interopérabilité ni conversion n'est inférée de l'usage commun d'AES-GCM.

CORE minSdk24, LLM minSdk29, VOICE/I et INTERFACE minSdk26 dans les révisions
inspectées. Aucun relevage de SDK appliqué ici. API24–28 nécessite une décision
et un adaptateur explicitement qualifié ; mini-PC requiert validation du backend,
poids/profil/licences et transport local, jamais une API cloud obligatoire.

Les changements de version majeure nécessitent négociation et refus explicite.
Un schéma v1 est fermé : même une addition de champ requiert négociation d'un
nouveau schéma/version avant envoi ; jamais déploiement destructif silencieux.
Le DTO CoreVoiceRequestV1 de VOICE005I est un contrat local spécialisé différent :
un futur adaptateur mappera ces enveloppes vers ce DTO après vérification des
capacités et consentements, sans présumer de contrôle émotionnel ou de vitesse.

## Validation exécutable

`scripts/contracts.py` valide uniquement les mots-clés utilisés par ces schémas,
refuse un mot-clé inconnu et ajoute les règles temporelles/voix/corrélation/bail.
Ce n'est pas une implémentation générale de JSON Schema. Les entiers de transport
sont exigés sans booléen ni représentation flottante ; les UUID sont canoniques,
les dates UTC. Un validateur JSON Schema tiers peut contrôler les mêmes fichiers,
mais ne remplace pas les règles sémantiques. Tests offline ≠ test IPC ou matériel.
