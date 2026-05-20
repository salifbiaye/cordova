# 📱 Collection d'Applications Mobiles Apache Cordova

Une suite d'applications mobiles hybrides performantes et ergonomiques développées avec **Apache Cordova**, **HTML5**, **CSS3 (Vanilla)**, et **JavaScript (jQuery)**. Ce dépôt comprend également des rapports techniques de présentation.

---

## 🚀 Vue d'Ensemble des Applications

La collection est composée de trois applications mobiles indépendantes illustrant divers aspects du développement mobile hybride (gestion du DOM, persistance des données, interactions tactiles) :

### 1. 📝 Ma Todo List (`todolist/`)
Une application moderne et intuitive de gestion de tâches.
- **Fonctionnalités :**
  - Ajout, modification, marquage (terminée/active) et suppression de tâches.
  - Compteur dynamique en temps réel des tâches restantes.
  - Filtres d'affichage : *Toutes*, *Actives*, *Terminées*.
  - **Interactions tactiles avancées (Swipe) :** Glisser vers la droite pour marquer une tâche comme terminée, glisser vers la gauche pour faire apparaître le bouton de suppression.
  - Animations fluides (CSS transitions & keyframes) lors de l'ajout et du retrait de tâches.
  - **Persistance :** Sauvegarde locale automatique via l'API `localStorage`.
- **Stack :** HTML5, CSS3 (animations personnalisées), JavaScript (ES6+), jQuery.

### 2. 📇 Contactel (`contactel/`)
Une application fluide de gestion de contacts avec une interface moderne en mode sombre/clair.
- **Fonctionnalités :**
  - CRUD complet (Créer, Lire, Mettre à jour, Supprimer) des contacts téléphoniques.
  - Formulaire de saisie modal élégant avec validation des champs obligatoires.
  - Catégorisation des contacts par groupes (*Famille*, *Amis*, *Travail*, *Autre*) avec badges de couleur associés.
  - Recherche dynamique en temps réel (par nom ou numéro de téléphone).
  - Génération automatique des initiales de l'avatar en fonction du nom.
  - **Persistance :** Stockage local des contacts dans le `localStorage`.
- **Stack :** HTML5, CSS3 (layout flexible et responsive), JavaScript, jQuery, FontAwesome.

### 3. ⚖️ Calculateur IMC (`imccalculator/`)
Un outil élégant pour évaluer la composition corporelle de l'utilisateur.
- **Fonctionnalités :**
  - Calcul instantané de l'Indice de Masse Corporelle (masse / taille²).
  - Contrôle et validation des entrées utilisateur (masse en kg, taille en m).
  - **Rendu visuel dynamique :** Cercle de progression SVG animé affichant le score.
  - Interprétation du résultat (Insuffisance, Normal, Surpoids, Obésité) et conseils personnalisés associés.
- **Stack :** HTML5, CSS3, JavaScript, SVG, FontAwesome.

---

## 📁 Structure du Projet

```text
cordova/
├── todolist/                   # Application de gestion de tâches
│   ├── config.xml              # Fichier de configuration Cordova
│   ├── package.json            # Dépendances & scripts de l'application
│   └── www/                    # Code source de l'interface (HTML/CSS/JS)
│
├── contactel/                  # Gestionnaire de contacts (Custom CSS & jQuery)
│   ├── config.xml
│   ├── package.json
│   └── www/
│
├── imccalculator/              # Calculateur d'IMC (Progress ring SVG)
│   ├── config.xml
│   ├── package.json
│   └── www/
│
├── rapports/                    # Rapports techniques PDF
│   ├── rapport_todo.pdf           # Rapport compilé en PDF (Todo List)
│   ├── rapport_contactel.pdf      # Rapport compilé en PDF (Contactel)
│   └── rapport_imc.pdf            # Rapport compilé en PDF (Calculateur IMC)
└── README.md                   # Ce fichier
```

---

## 🛠️ Installation et Exécution

### Prérequis
- [Node.js](https://nodejs.org/) (version LTS recommandée)
- [Android Studio](https://developer.android.com/studio) (pour compiler/émuler sur Android)
- Cordova CLI installé globalement :
  ```bash
  npm install -g cordova
  ```

### Lancement d'un Projet

Pour exécuter l'une des applications (par exemple `todolist`) :

1. **Se positionner dans le dossier de l'application :**
   ```bash
   cd todolist
   ```

2. **Ajouter la plateforme de développement (ex: Android) :**
   ```bash
   cordova platform add android
   ```

3. **Lancer l'application sur un émulateur ou appareil connecté :**
   ```bash
   cordova run android
   ```

4. **Tester dans le navigateur (Serveur de développement) :**
   ```bash
   cordova serve
   ```
   *Ou ouvrez simplement le fichier `www/index.html` dans votre navigateur.*

---

## 📊 Rapports

### 📄 Rapports PDF
Les rapports techniques de chaque application se trouvent sous format PDF dans le dossier [rapport/](file:///c:/Users/DELL/Downloads/cordova/rapport). Ils détaillent le fonctionnement technique et la conception de chaque application.
