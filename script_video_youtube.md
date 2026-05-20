# Script video YouTube - Presentation Todo List Cordova

Objectif: presenter rapidement le code au debut, puis montrer surtout l'application.
Format conseille: 5 a 6 minutes maximum.

## Plan global

| Temps | Ecran | Ce que tu dis |
| --- | --- | --- |
| 0:00 - 0:15 | Repo / dossiers | "Bonjour, dans cette video je vais presenter mon application mobile Todo List developpee avec Apache Cordova. Je vais d'abord montrer rapidement la structure du code, puis je passerai a la demonstration de l'application. En bonus, je montrerai aussi deux autres mini-applications: Contactel et le Calculateur IMC." |
| 0:15 - 2:00 | Code Todo List | "La partie code sera breve: je vais montrer les fichiers essentiels qui font fonctionner l'application." |
| 2:00 - 4:30 | Application Todo List | "Maintenant, place a la demonstration de l'application." |
| 4:30 - 5:30 | Bonus Contactel + IMC | "En bonus, voici deux autres applications realisees avec la meme logique Cordova." |
| 5:30 - 6:00 | Repo + conclusion | "Pour finir, je montre rapidement le depot et les fichiers du projet." |

## Partie 1 - Introduction

### A montrer

- Ouvrir le dossier du projet: `C:\Users\DELL\Downloads\cordova`
- Montrer les dossiers:
  - `todolist`
  - `contactel`
  - `imccalculator`
  - `rapport`

### Texte a dire

"Bonjour a tous. Dans cette video, je vais presenter mon projet Cordova. L'application principale est une Todo List, c'est-a-dire une application de gestion de taches. Le but est de pouvoir ajouter des taches, les marquer comme terminees, filtrer les taches, les supprimer, et garder les donnees meme apres fermeture de l'application. Je vais commencer par une presentation rapide du code, en moins de deux minutes, puis je montrerai l'application en fonctionnement."

## Partie 2 - Code rapide, maximum 2 minutes

### 0:15 - 0:35: Structure Cordova

#### A montrer

- `todolist/config.xml`
- `todolist/package.json`
- Le dossier `todolist/www`

#### Texte a dire

"Ici, on voit la structure du projet Cordova. Le fichier `config.xml` contient la configuration de l'application, comme l'identifiant, la version et le fichier de demarrage. Le fichier important pour l'interface est dans le dossier `www`, car Cordova transforme cette partie web en application mobile Android."

### 0:35 - 0:55: HTML

#### A montrer

- `todolist/www/index.html`
- Montrer rapidement:
  - le titre `Ma Todo List`
  - les filtres `Toutes`, `Actives`, `Terminees`
  - la liste `task-list`
  - le bouton d'ajout
  - la modal

#### Texte a dire

"Dans `index.html`, j'ai construit la structure de l'application. Il y a un header avec le nombre de taches restantes, trois boutons pour filtrer les taches, une liste vide qui sera remplie avec JavaScript, un bouton flottant pour ajouter une tache, et une fenetre modale pour saisir une nouvelle tache."

### 0:55 - 1:25: JavaScript

#### A montrer

- `todolist/www/js/index.js`
- Montrer:
  - `STORAGE_KEY = 'todos'`
  - `state`
  - `load()`
  - `persist()`
  - `addTask()`
  - `toggleTask()`
  - `deleteTask()`
  - `setFilter()`

#### Texte a dire

"Dans le fichier JavaScript, toute la logique est centralisee. Les taches sont stockees dans un tableau `state.tasks`. Au demarrage, la fonction `load()` recupere les taches depuis le `localStorage`, et la fonction `persist()` sauvegarde les modifications. Quand j'ajoute une tache, je cree un objet avec un identifiant, un texte et un statut `done`. Ensuite, je sauvegarde et je rafraichis l'affichage."

"J'ai aussi une fonction pour cocher ou decocher une tache, une fonction pour supprimer, et une fonction pour filtrer entre toutes les taches, les taches actives et les taches terminees."

### 1:25 - 1:45: Swipe mobile

#### A montrer

- Dans `index.js`, la partie `bindSwipe()`
- Montrer `touchstart`, `touchmove`, `touchend`

#### Texte a dire

"La partie la plus interessante est le swipe. J'utilise les evenements tactiles `touchstart`, `touchmove` et `touchend`. Si l'utilisateur glisse vers la droite, la tache est marquee comme terminee. S'il glisse vers la gauche, le bouton de suppression apparait, puis la tache peut etre supprimee. Cela donne une interaction plus proche d'une vraie application mobile."

### 1:45 - 2:00: CSS

#### A montrer

- `todolist/www/css/index.css`
- Montrer:
  - `#btn-add`
  - `.task-content`
  - `.filter-btn.active`
  - animations `slideIn`, `flashGreen`, `slideOutLeft`

#### Texte a dire

"Enfin, dans le CSS, j'ai gere le design mobile: couleurs, bouton flottant, cartes de taches, filtres actifs et animations. Par exemple, quand une tache est ajoutee, cochee ou supprimee, une animation rend l'application plus fluide."

Transition:

"Maintenant que le code principal est presente, je passe a la demonstration de l'application."

## Partie 3 - Demonstration de la Todo List

### 2:00 - 2:20: Ecran d'accueil

#### A montrer

- Lancer l'application Todo List
- Montrer le titre, le compteur et l'etat vide

#### Texte a dire

"Voici l'ecran principal de l'application. En haut, on retrouve le nom de l'application et le nombre de taches restantes. Pour l'instant, la liste est vide, donc l'application affiche un message invitant a ajouter une premiere tache."

### 2:20 - 2:50: Ajouter des taches

#### A montrer

- Cliquer sur le bouton `+`
- Ajouter par exemple:
  - "Reviser le cours Cordova"
  - "Preparer la presentation"
  - "Envoyer le rapport"

#### Texte a dire

"Pour ajouter une tache, je clique sur le bouton plus. Une fenetre s'ouvre en bas de l'ecran. Je saisis le nom de la tache, puis je clique sur enregistrer. La tache apparait directement dans la liste, et le compteur se met a jour automatiquement."

### 2:50 - 3:15: Cocher / terminer une tache

#### A montrer

- Cliquer sur une tache ou la checkbox
- Montrer le texte barre et le compteur qui change

#### Texte a dire

"Quand une tache est terminee, je peux la cocher. L'application change son apparence: la tache est barree, la coche apparait, et le nombre de taches restantes diminue. Cela permet de voir rapidement ce qu'il reste a faire."

### 3:15 - 3:40: Filtres

#### A montrer

- Cliquer sur:
  - `Toutes`
  - `Actives`
  - `Terminees`

#### Texte a dire

"J'ai aussi ajoute un systeme de filtres. Le bouton `Toutes` affiche toute la liste. Le bouton `Actives` affiche uniquement les taches qui ne sont pas encore terminees. Le bouton `Terminees` affiche uniquement les taches deja completees. Ce filtrage est fait directement en JavaScript a partir du tableau des taches."

### 3:40 - 4:05: Swipe et suppression

#### A montrer

- Faire un swipe vers la gauche sur une tache
- Montrer l'icone supprimer
- Supprimer la tache
- Eventuellement faire un swipe vers la droite pour terminer une tache

#### Texte a dire

"Pour rendre l'application plus mobile, j'ai ajoute une interaction par glissement. En glissant vers la gauche, le bouton de suppression apparait. Je peux ensuite supprimer la tache. En glissant vers la droite, je peux marquer rapidement une tache comme terminee. C'est une fonctionnalite simple, mais elle rend l'application plus agreable a utiliser."

### 4:05 - 4:30: Sauvegarde locale

#### A montrer

- Revenir rapidement dans `todolist/www/js/index.js`
- Montrer:
  - `var STORAGE_KEY = 'todos';`
  - `load()`
  - `persist()`
  - `localStorage.getItem(...)`
  - `localStorage.setItem(...)`

#### Texte a dire

"Pour la sauvegarde, j'utilise `localStorage`. Comme je teste ici sur un emulateur Android, je ne vais pas forcement le demontrer en fermant et relancant l'application. Mais dans le code, on voit bien la logique: `load()` recupere les anciennes donnees et `persist()` enregistre les nouvelles donnees apres chaque ajout, suppression ou modification."

"Il faut aussi preciser que ce stockage est local a l'application et a l'emulateur. Ce n'est pas une base de donnees en ligne. Pour une version plus avancee, on pourrait utiliser SQLite ou une base distante."

## Partie 4 - Bonus: Contactel

### A montrer

- Ouvrir `contactel`
- Montrer:
  - ajout d'un contact
  - nom, telephone, email, groupe
  - recherche
  - filtres par groupe
  - modifier / supprimer

### Texte a dire

"En bonus, j'ai aussi realise une application de gestion de contacts appelee Contactel. Le principe est proche de la Todo List, mais adapte aux contacts. On peut ajouter un contact avec son nom, son telephone, son email et son groupe. Ensuite, on peut rechercher un contact, filtrer par Famille, Amis, Travail ou Autre, modifier les informations et supprimer un contact."

"Cette application utilise aussi le `localStorage`, donc les contacts sont sauvegardes localement."

## Partie 5 - Bonus: Calculateur IMC

### A montrer

- Ouvrir `imccalculator`
- Entrer:
  - masse: `70`
  - taille: `1.75`
- Cliquer sur `Calculer l'IMC`
- Montrer:
  - resultat numerique
  - categorie
  - conseil
  - cercle anime

### Texte a dire

"Le deuxieme bonus est un calculateur d'IMC. L'utilisateur entre sa masse en kilogrammes et sa taille en metres. L'application calcule ensuite l'IMC avec la formule: masse divisee par taille au carre. Le resultat est affiche avec une categorie, par exemple poids normal, surpoids ou obesite, et un court conseil."

"J'ai aussi ajoute une petite animation circulaire pour rendre le resultat plus visuel."

## Partie 6 - Montrer le repo et conclure

### A montrer

- Revenir au dossier principal
- Montrer:
  - `todolist/www/index.html`
  - `todolist/www/css/index.css`
  - `todolist/www/js/index.js`
  - `contactel/www`
  - `imccalculator/www`
  - `rapport`

### Texte a dire

"Pour terminer, voici le depot du projet. On retrouve l'application principale Todo List, les deux applications bonus Contactel et Calculateur IMC, ainsi que les rapports. Chaque application garde la meme structure Cordova: un fichier HTML pour la structure, un fichier CSS pour le design et un fichier JavaScript pour la logique."

"Dans le dossier `rapport`, j'ai aussi prepare les PDF detailles des trois applications: le rapport de la Todo List, le rapport de Contactel et le rapport du Calculateur IMC. La video montre la partie pratique, et les documents PDF completent avec le resume detaille, les fonctionnalites et l'explication technique de chaque application."

"Ce projet m'a permis de travailler sur une application mobile avec Cordova, la manipulation du DOM, les evenements utilisateur, le stockage local, les filtres, les formulaires et les interactions tactiles. Merci d'avoir regarde cette presentation."

## Version courte a apprendre par coeur

"Dans cette video, je presente mon application Todo List developpee avec Cordova. Le projet est organise autour du dossier `www`, qui contient le HTML, le CSS et le JavaScript. Dans le HTML, j'ai la structure de l'application: le header, les filtres, la liste des taches, le bouton d'ajout et la modal. Dans le JavaScript, je gere l'ajout, la suppression, le filtrage, le statut termine et la sauvegarde avec `localStorage`. J'ai aussi ajoute le swipe pour une meilleure experience mobile. Dans le CSS, j'ai travaille le design, les couleurs, les animations et le bouton flottant."

"Dans l'application, je peux ajouter une tache, la cocher quand elle est terminee, filtrer les taches actives ou terminees et supprimer une tache. Pour la sauvegarde, j'utilise `localStorage`: je l'explique dans le code avec les fonctions `load()` et `persist()`, car je teste l'application sur un emulateur. En bonus, j'ai aussi realise Contactel pour gerer des contacts, et un Calculateur IMC pour calculer l'indice de masse corporelle. A la fin, je montre aussi les trois PDF de rapport qui resument chaque application en detail."

## Conseils de tournage

- Ne lis pas tout mot a mot: parle naturellement avec ce document comme guide.
- Pour le code, ne depasse pas 2 minutes.
- Zoom seulement sur les fonctions importantes.
- Dans l'application, prends ton temps: c'est la partie la plus importante.
- Prepare 3 taches avant de filmer ou ajoute-les en direct.
- Evite de scroller trop vite dans le code.
- Termine toujours par le repo pour montrer que le projet est complet.
