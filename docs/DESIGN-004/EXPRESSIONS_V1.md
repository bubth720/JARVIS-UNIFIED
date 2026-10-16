# Architecture EXPRESSIONS V1 — réutiliser le catalogue et VOICE

**Proposition documentaire, pas une bibliothèque600–1000 déjà livrée.** Lire les
[réserves ADR](RESPONSABILITES_ET_ADR.md) et [sources](SOURCES.md).
Aucun moteur, routeur autonome CORE, base concurrente ou système vocal créé.

## Point de départ vérifié

LLM mission003-catalogue à0b5eba7, conservée dans003B1756e29 :
AnswerRecord / KnowledgeSource / IntentRouter du domaine, CatalogueStore SQLite,
CatalogueJson portable et huit réponses DEMO (neuf variantes au total).
Tables : answers, variants, phrases, phrase_search FTS4, revisions, catalogue_meta.
Révisions optimistes, tombstones, import atomique, export courant en flux ;
l’historique n’est pas dans l’export JSON. La suppression logique ne purge pas
le texte. Embeddings non actifs ; pas de chargement LLM pour une réponse catalogue.

Contraintes actuelles à conserver : ID/intention `[a-z0-9._-]`, longueur1–64 ;
1–12 exemples par réponse (≤500 caractères), 1–8 variantes (≤2000), titre≤160,
catégorie≤64, révision entière positive ;5000 IDs suppressions incluses ; import8Mio,
volume courant réservé pour export et SQLite plafonnée64Mio. Version JSON1,
neuf champs exacts par réponse : id,intent,title,category,revision,examples,
variants,origin,deleted. Origines DEMO/USER/SYNTHETIC uniquement.

IntentRouter conserve négation, nombres et types interrogatifs, candidats bornés20,
seuils prudents/clarification, rotation déterministe de variantes par session et
fallback LLM soumis aux protections. Ce n’est pas une compréhension sémantique
générale. Les doublons concurrents de même intention peuvent déclencher une
clarification : ne pas les multiplier pour contourner les huit variantes.

## Objectif éditorial et taille

«600–1000 formulations» = nombre de textes **variants** distincts revus, pas nombre
d’exemples de requêtes, ni records, ni données synthétiques de benchmark.
Cible de travail800 =200 intentions précises ×4 variantes. Plage600–1000 après
curation, pas obligation d’atteindre un chiffre au prix de réponses inexactes.
Conserver un record par sens/intention stable quand possible ; les variantes
restent équivalentes. Ni1500 fixtures SYNTHETIC ni huit DEMO ne comptent comme
800 réponses conversationnelles validées. Un pack réel sera développé dans LLM,
pas copié dans UNIFIED ; aucun texte personnel dans Git.

| Famille proposée | Nombre indicatif d’intentions précises | Variantes cible | Condition essentielle |
|---|---|---|---|
| Accueil et reprise | 20 | 80 | Moment/contexte fournis et vérifiés, jamais devinés |
| Disponibilité et aide | 20 | 80 | Capacités connues, pas promesse générale |
| Clarification et reformulation | 20 | 80 | Ne pas inventer une option disponible |
| Acquittements conversationnels | 20 | 80 | Accusé de réception ≠ action effectuée |
| Refus et permissions | 20 | 80 | Refus exact, aucune demande de secret dans le dialogue |
| Statuts de tâche et attente | 20 | 80 | État reçu du propriétaire, périmé clairement indiqué |
| Documents et recherche | 20 | 80 | Source/capacité réelles, pas « document trouvé » sans preuve |
| Mémoire et confirmations | 20 | 80 | Proposition/confirmation/enregistrement distincts |
| Hors ligne et appareils | 20 | 80 | Capacités du pair courant, absence PC sans fausse panne locale |
| Annulation, erreurs et reprise | 20 | 80 | Arrêt demandé ≠ fin native ≠ opération défaite |
| Total cible de planification | 200 | 800 | À qualifier ; pas contenu déjà produit |

Phases éditoriales :20 intentions/60 variantes pilote ;100/300 ;200/800 ; extension
jusqu’à1000 uniquement si nouveaux cas utiles. Chaque lot a provenance/licence,
revue humaine, exemples positifs et négatifs, contexte admissible et critères de
vérité. Les paramètres de l’énoncé (noms, dates, états) ne sont pas des variantes
factuelles : il faut un rendu borné explicite, **non supporté aujourd’hui par le
format littéral**. Pas de substitution de placeholders ou de code dans des chaînes
importées. Commencer par formulations littérales neutres compatibles JSON1.

## Parcours proposé et réutilisation

L’accès au composant catalogue depuis CORE reste un port local futur, pas une
connexion déjà présente. Si le module est absent/incompatible, CORE garde son
parcours historique autonome ; aucune copie de catalogue dans CORE ou dépendance
au PC n’est ajoutée pour masquer l’absence.

CORE reçoit l’événement ou la demande, autorise le parcours, vérifie fraîcheur,
capacité et source de vérité ; le catalogue LLM fournit candidats/clarification,
sans décision d’outil. CORE fixe le texte final et son éventuelle diffusion ;
VOICE synthétise ce texte avec profil choisi et consentement valide.

Préserver IntentRouter existant. La méthode actuelle route(question) n’accepte
pas un contexte arbitraire et ne connaît pas les futurs événements CORE ; ne pas
la présenter comme contextuelle déjà opérationnelle. Pour V1 pilote : variantes
neutres et rotation actuelle. Pour variantes conditionnelles : proposer dans LLM
une sélection contextuelle typée, propriété du **même composant catalogue**, avec
métadonnées versionnées dans son stockage existant après décision, aucun second
index/routeur dans CORE ou NEXUS. CORE fournit seulement les faits/contextes
admissibles et conserve décisions/confirmations.

Ne pas ajouter des champs contextuels au JSON1 fermé. Option à étudier : extension
versionnée et tables de métadonnées dans la même base, avec migration réversible ;
ou métadonnées de pack séparées, appartenant au même catalogue, sans recopier
les textes. Aucun choix de schéma effectué ici. Les ID de variantes actuelles sont
leurs positions : le tuple recordID/révision/position/digest reste lié à la version,
jamais position seule comme identité permanente.

Si ambiguïté, négation/numéro non couvert, candidats dépassés, contexte périmé ou
capacité indisponible : clarification/refus explicite. Pas de génération forcée
pour masquer une absence ; fallback LLM autorisé seulement selon politique CORE
et sécurité matérielle existante. Un texte « oui » n’autorise aucune mémorisation,
aucune action ou partage sans la procédure de confirmation du contenu exact.
Un contenu rédigé par un document/LLM n’est pas un pack éditorial automatiquement fiable.

Préférences de concision/vouvoiement peuvent sélectionner des formulations de même
sens une fois contrat qualifié. Ni persona ni label HUMOROUS ne prouve une émotion
acoustique. Pas de réécriture cachée du texte par la voix. Ne pas réutiliser les
DEMO « cette application n’a pas de réseau » comme promesse de tous les futurs
modules connectés : portée et révision éditoriales doivent suivre l’application.

## Extensions et transfert des données éditoriales

Propriétaire technique actuel : LLM ; CORE n’ouvre pas directement catalogue.db.
Réutiliser CatalogueJson et merge/save, sans écrire les tables à distance. Pack
éditeur identifié/versionné et approuvé, différences prévisualisées ; ID et révision
stables, aucune génération auto-apprise issue d’une conversation personnelle.
Les origines actuelles ne contiennent pas EDITORIAL : provenance/identité d’éditeur
à proposer dans métadonnées de pack, ne pas inventer une nouvelle enum JSON1.

Une même révision divergente doit toujours refuser le lot ; compteur revision seul
ne résout pas deux éditions concurrentes. Pour un pilote sûr, éditeur unique par
pack et imports sérialisés. Plusieurs appareils éditeurs = branche de conflit et
nouvelle révision validée sur une base commune ; interdiction de gonfler le numéro
pour écraser une modification. Toute synchronisation de catalogue est opt-in et
séparée du contenu personnel et des mises à jour logicielles. Pas de copie du
fichier SQLite ni d’un index FTS déjà construit.

## Cache audio facultatif : extension VOICE, pas nouvelle pile

Existant lu : PrivatePcmStore conserve une phrase PCM32 complète≤20s/480000 samples,
intégrité SHA et activation atomique ; QualityABStore possède seulement deux slots
A/B avec texte/graine/pack/tensors et metadata. Les wrappers Identity/Expression
lient profil et conditioning. Cela **n’est pas** un cache de1000 phrases. Reprendre
ces primitives après audit, ne pas modifier leur sémantique A/B pour en faire
silencieusement un cache conversationnel.

Proposition : cache VOICE privé, dérivé et révocable, **désactivé par défaut**,
activation distincte consentie par identité/profil et type d’expressions. Commencer
par texte éditorial statique non personnel ; données personnalisées et résultats
de recherche exclus. Chaque lecture revérifie autorisation, profil actif,
compatibilité, digest et fraîcheur du texte ; un hit ne dispense pas de consentement.

Clé logique privée comprenant : moteur/version de rendu, digest pack exact,
profil/révision et conditioning exacts, texte final exact/revision catalogue/position,
normaliseur/rendu, paramètres graine/LSD/température, plan de pauses et format
PCM/fréquence/canaux. Sérialisation canonique définie avant implémentation ; pas
concaténation ambiguë ni hash public de texte privé. La clé ne révèle rien dans
Git/logs. Elle ne rend pas un profil portable vers un autre moteur.

Invalider sur édition/tombstone du catalogue, profil/pack/moteur différent,
changement de paramètres, consentement retiré ou expiration d’état. Lecture
d’un ancien état de tâche interdite même avec PCM valide. Une résolution d’erreur
ne réutilise pas un audio affirmant un succès. Révocation interdit immédiatement
lecture et nouvelle génération ; purge locale sûre et clés à définir, sans promesse
d’effacement physique absolu. Rien n’est envoyé à la montre/PC par SYNC V1.

Bornes de départ **proposées, non mesurées** : max20 entrées ET32Mio au total,
max20s/entrée, vérification avant réservation ; éviction LRU des seuls dérivés
non utilisés, jamais originaux/profils. 1000 phrases de20s à24kHz Float32 feraient
~1,92Go : ne pas pré-générer toute la bibliothèque. Qualifier une fenêtre plus
petite sur matériel faible ; cache montre absent par défaut. Génération au besoin,
aucun moteur chargé en permanence et aucune concurrence lourde forcée pour remplir
un cache ; l’arbitre global reste à décider. Cache hit n’implique pas fin audible.

Le stockage privé sandbox existant n’est pas annoncé chiffré par le code cache.
Proposer protection au repos/clé plateforme adaptée pour les nouveaux dérivés
personnels, après choix matériel et menace ; ne pas affirmer une migration crypto
réalisée. Export, profils et cache ont politiques distinctes. Lire en flux/buffers
bornés, audio focus/arrêt et restitution intégrale préservés ; pas de streaming ou
de gain de latence annoncé sans mesures. Texte immédiat si VOICE absent/refusé ;
aucun remplacement générique de la voix personnelle à l’insu de l’utilisateur.

## Vérifications de qualification futures

E1 pack600–1000 compté sur variantes uniques, mêmes limites existantes ; E2 négation,
nombres, homonymes, demandes adverses, contexte absent/périmé ; E3 collision de même
intention et compteur20 ; E4 import atomique/idempotent, révision concurrente et
non-résurrection ; E5 aucune allocation/native charge LLM pour réponse simple ;
E6 sélection ne produit aucune action ni souvenir ; E7 cache mauvais profil/pack,
corruption, révocation et quota ; E8 PCM comparable à génération complète, annulation
et focus ; E9 froid/chaud/hit/miss CPU/PSS/thermique réels séparés du cloud ;
E10 aucune donnée privée dans fixtures. Corpus de test tenu à part des exemples
éditeur, métriques faux positifs/clarifications/fallback par intention, pas seulement
score global. Budget et seuils fixés après mesures, aucun abaissement de protection.
**Aucun de ces essais produit/Android n’est exécuté dans DESIGN-004.**
