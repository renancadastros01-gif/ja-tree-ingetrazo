# JA Tree pour IngeTrazo

**0.1.0 · Julio Angulo · IngeTrazo 0.5.7 / API d’extensions 2**

Un panneau latéral pour explorer et organiser les groupes, composants et plans
de coupe natifs. Il comprend la recherche, la sélection synchronisée, la
visibilité, l’organisation par glisser-déposer, les étiquettes, le cadrage et
l’historique natif d’annulation/rétablissement. Les modifications sont
enregistrées dans le fichier IGZ du modèle.

## Installation

1. Décompressez **JA_Tree_v0.1.0.zip**.
2. Dans IngeTrazo, ouvrez **Extensions → Open plugins folder**.
3. Copiez le dossier **outliner** complet, avec ses icônes et ses traductions.
   Cet identifiant interne conserve les préférences de l’installation précédente.
4. Redémarrez IngeTrazo et ouvrez **Extensions → JA Tree…**.

L’archive contient le modèle d’exemple **Ejemplo_JA_Tree.igz**. Aucune dépendance
supplémentaire n’est nécessaire. Pour une mise à jour, remplacez l’ancien dossier
outliner.

## Langue et commandes

Dans le bouton d’options du panneau, choisissez **Langue → Français / English /
Español**. Le changement est immédiat et mémorisé. **Automatique (IngeTrazo)**
suit la langue du programme et utilise l’anglais pour les langues non prises
en charge. Le français peut être choisi ici même si IngeTrazo ne le propose pas.
Les noms et étiquettes saisis par l’utilisateur sont conservés.

Cliquez sur un nom pour sélectionner ; double-cliquez ou appuyez sur Entrée pour
modifier ; F2 pour renommer ; Échap pour quitter un niveau d’édition ; F pour
cadrer la sélection. Cliquez sur l’œil pour masquer/afficher un objet. Glissez
sur un groupe pour imbriquer, ou sur Modèle pour déplacer à la racine. Désactivez
le tri A–Z pour réordonner les objets du même niveau. La sélection multiple
s’effectue dans un même conteneur. Le clic droit donne accès aux étiquettes,
au renommage, à la visibilité, à la suppression et au cadrage. Les indicateurs
de coupe activent/désactivent les coupes ; une seule peut être active.

## Portée

La réorganisation conserve les positions globales, les maillages partagés,
les matériaux et les données des extensions. Les verrouillages par étiquette
sont respectés ; IngeTrazo 0.5.7 n’a pas de verrou individuel natif pour les
groupes. Les plans de coupe restent au niveau du modèle. Réassemblez une vue
éclatée avant de réorganiser. Le renommage concerne l’instance choisie ; les
autres copies d’un composant ne sont pas automatiquement réorganisées. Le
panneau masque la colonne des étiquettes lorsqu’il devient étroit.

Vérifié avec le code réel d’IngeTrazo 0.5.7, commit 6be29fe. Les autres versions
0.x nécessitent une vérification. Fermez IngeTrazo et retirez le dossier outliner
pour désinstaller. Le [guide espagnol détaillé](README.md) décrit le développement
et les comportements supplémentaires.

## Code ouvert

JA Tree **0.1.0** est la première version préparée pour publication. Le projet est
distribué sous **GPL-3.0-or-later** : [licence](LICENSE), [mentions](NOTICES.md),
[contribution et compilation](CONTRIBUTING.md) et [changements](CHANGELOG.md).
Un ZIP installable et une archive du code source avec les tests sont fournis.
