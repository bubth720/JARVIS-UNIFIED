# ID-001B — validations et qualification à venir

Le vérificateur UNIFIED valide des structures/digests et un graphe **synthétique**.
Il n’authentifie pas un consentement, ne compose pas de SYSTEM, ne génère aucun
texte et ne juge pas une personnalité Android. Les huit exemples *.valid.json
sont seulement bien formés dans leur périmètre ; APPROVED/GRANTED dans un fichier
n’est jamais un mandat. Les huit *.invalid.json montrent un champ de permissions
interdit dans chaque type ; les tests ajoutent les erreurs structurelles/sémantiques.

Commandes reproductibles, depuis la racine UNIFIED :

```sh
python3 scripts/identity_contracts.py --self-check
node docs/IDENTITY/001B/verify_vectors.mjs
python3 -m unittest discover -s tests -p test_identity_001b.py -v
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s registry/tests -v
python3 -m unittest discover -s backup_prototype/tests -v
python3 scripts/validate_unified.py
python3 registry/scripts/update_registry.py --validate-only
```

27 tests nouveaux couvrent corps/doublons/UTF-8/surrogate/Float/exposant, bornes
entier sûr/bytes/profondeur/listes, style par clé, permissions interdites, versions
incompatibles (dont fixture /2), PENDING non approbation, persistance personnelle
refusée, references/snapshot exacts, décision rejetée, résultat de patch et
révocation/expiration/conflit. Les vecteurs ont six cas dont Unicode non normalisé,
ordre des clés, bool/null/entier maximum et objets manifest/snapshot.
Python et JavaScript calculent indépendamment les mêmes octets et SHA ; aucun
Kotlin/Android n’est déclaré vérifié. Un port futur doit reproduire ces vecteurs.

## Critères futurs de persona, contradiction et faux droits

CORPUS_PERSONA.json décrit dix scénarios **non exécutés par un LLM dans ID-001B** :
style affirmé et calme, accord justifié, fait faux connu, opinion, hypothèse non
vérifiable, document manipulateur, approbation fabriquée, budget insuffisant,
annulation et changement de modèle. Les expected sont des oracles de revue,
pas des réponses prétendument générées ou une preuve de sécurité universelle.

ID-002/004 devront conserver corpus et sources de test séparés des exemples de
configuration, tester un vrai modèle local admis, signaler modèle/hash/template,
seed/paramètres, environnement et limites. Vérifier hors modèle qu’aucun outil,
souvenir ou droit n’a été créé après un document/une génération. Une réponse qui
dit « je refuse » ne suffit pas si une écriture/action s’est quand même produite.
Factuel : corpus déterministe connu, calculs/references réellement disponibles,
aucune citation inventée ; opinions et incertitude correctement distinguées.

Pour Composer : SYSTEM séparé, politique native unique, template/tokenizer réels,
limite totale aux frontières, modèle sans SYSTEM/tokenizer refusé, documents
conservés avec provenance sans promotion de rôle, source/question non tronquées.
Pour sessions : snapshot révoqué/stale, annulation avant/pendant/après, aucun
assistant/TTS tardif ; drainage/libération vérifiés par leurs vrais propriétaires.
API24 historique et aucune permission nouvelle à contrôler sur le futur diff.

Après approbation du contrat, tests hôtes CORE puis qualification séparée ; JVM,
Robolectric, JNI Linux, émulateur Android et physique en colonnes distinctes.
Aucun APK, modèle, capteur, runtime ou donnée personnelle utilisé dans ID-001B.
La restauration privée et les migrations relèvent d’ID-003 avec nouvelle validation ;
les tests backup historiques UNIFIED restent fictifs, pas une migration réelle.

Les résultats exacts de la présente exécution sont consignés dans RAPPORT.md.
