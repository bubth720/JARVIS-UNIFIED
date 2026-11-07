# Rollback de coordination et réception

Base `a73c1571f3e1dd0acd50e87b9742fbe2214a93d2`, tree `0226f108b72f44ec90a5640b8ca8f77d058fc686`. Cette PR n'ajoute que rapports/outils/workflow ; tous les fichiers préexistants sont figés. Abandonner la branche ou fermer la PR sans modifier les autres branches suffit. Aucun reset/force-push, migration, modèle, clé ou runtime à annuler.

Pour une APK M51 fournie séparément : utiliser son applicationId et certificat exacts, jamais désinstaller l'ancien paquet pour contourner une signature différente. Les données sont isolées ; la procédure d'installation/désinstallation personnelle reste soumise à accord explicite. La disparition d'une interface n'est pas preuve de suppression des sauvegardes ou fichiers originaux.

Un retour de code ne prouve pas drainage/déchargement d'un futur modèle. UNKNOWN/CLEANUP_FAILED conservent la quarantaine. Il faut une récupération native explicitement qualifiée ; aucun second moteur ni bail fictif. Cette coordination ne lance aucune tentative de récupération.
