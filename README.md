# BrickSearch : Recherche de pièces LEGO

Bienvenue dans ce dépôt GitHub dédié au projet **Recherche de pièces LEGO**. Ce document fournit une première vue d’ensemble du contexte, de la problématique ainsi que de l’objectif de ce projet.

## Contexte
Les passionnés de LEGO connaissent souvent la difficulté de retrouver une pièce précise parmi plusieurs centaines de briques mélangées. Que vous soyez un collectionneur chevronné ou un simple amateur, la recherche d’une brique en particulier peut rapidement se révéler chronophage. L’idée derrière ce projet est de s’appuyer sur des outils automatisés, de la documentation existante et une base de données de pièces pour accélérer et faciliter l’identification, puis la localisation de la brique souhaitée.

## Problématique
- **Complexité des références** : LEGO propose de très nombreuses pièces, chacune possédant des numéros d’identification, des variations de couleurs.
- **Organisation des inventaires** : La recherche efficace d’une pièce demeure un défi, surtout quand les quantités deviennent importantes.
- **Gain de temps et fiabilité** : L’identification manuelle de chaque pièce peut prendre un temps considérable.

## Objectif
Le principal objectif est de développer un outil ou un ensemble de scripts permettant :
1. D’identifier rapidement une pièce LEGO à partir d’une photo ou d’une vidéo.
2. De fournir à l’utilisateur des informations pertinentes sur la pièce recherchée (numéro, nom exact, disponibilité, prix indicatif, etc.).

En centralisant et en automatisant ces tâches, le projet **Recherche de pièces LEGO** vise à rendre la recherche plus rapide et plus précise, que ce soit pour des utilisateurs occasionnels ou des utilisateurs avertis.

---

## Structure du projet

Le dépôt s’organise de la manière suivante :

```
.
├── data
│   ├── annotations_files
│   │   └── Annotation_train_set.json
│   ├── dataset
│   │   ├── data.yaml
│   │   ├── test
│   │   ├── train
│   │   └── val
│   ├── model
│   └── raw
├── docs
├── outputs
│   ├── images_annotees
│   ├── json_annotation_img
│   ├── output_models
│   └── video_annotees
├── scripts
│   ├── apk_app
│   └── Notebooks
├── tools
│   └── via-2.0.12
├── LICENSE
└── README.md
```

- **`data/`** : Contient les jeux de données (images brutes, labels, fichiers d’annotations).  
  - **`annotations_files/Annotation_train_set.json`** : Exemple de fichier d’annotations généré via le VGG Image Annotator (VIA).  
  - **`dataset/`** : Répertoire principal pour l’entraînement, la validation et le test (sous-répertoires `train`, `val` et `test`).  
  - **`model/`** : Stocke les poids pré-entraînés.  
  - **`raw/`** : Fichiers d’images brutes, non annotées.

- **`docs/`** : Rassemble la documentation associée au projet (ex. : Objectif, Étapes, guides, fichiers bureautiques).

- **`outputs/`** : Contient les résultats (images ou vidéps annotées, JSON d'annotation, rapports de performance et poids finaux du modèle).

- **`scripts/apk_app/`** :  sources de l'application android de détection 

- **`scripts/Notebooks/`** :  
  - **`conversion-YoloA_from_VggIA.ipynb`** : Notebook pour convertir ou adapter les annotations du format VGG Image Annotator (VIA) en un format exploitable par YOLO.  
  - **`test_model.ipynb`** : Permet de tester le modèle entraîné sur un ensemble de données de test.  
  - **`train_model.ipynb`** : Lance le processus d’entraînement du modèle YOLO sur les images annotées.
  - **`test_model_video_fast.ipynb`** : Permet de tester le modèle entraîné sur un flux video.  

- **`tools/via-2.0.12/`** : Fichiers relatifs à l’outil VGG Image Annotator (VIA), utilisé pour la création et la gestion des annotations.

- **Fichiers de configuration** :  
  - **`LICENSE`** : Conditions de licence et de redistribution du projet.  

---

## Annotation des images avec VIA (VGG Image Annotator)

Cette étape est **essentielle** pour créer des jeux de données correctement annotés, utilisables par les algorithmes de détection d’objets.

1. **Installation ou utilisation de VIA**  
   - Vous pouvez vous rendre sur le [dépôt GitHub officiel de VIA](https://www.robots.ox.ac.uk/~vgg/software/via/) pour télécharger l'outil.
   - Ouvrez simplement le fichier `index.html` dans votre navigateur.  

2. **Préparation des images**  
   - Placez vos images dans un répertoire (par exemple, `data/raw` ou `data/dataset/train`).  
   - Lancez VIA et créez un **nouveau projet** en important toutes les images à annoter.

3. **Création des annotations**  
   - Dans VIA, sélectionnez chaque image et dessinez des bounding boxes autour des pièces LEGO à reconnaître.  
   - Attribuez un label à chacune de ces zones : par exemple, le type de pièce, sa couleur.  

4. **Exportation des annotations**  
   - Une fois l’annotation terminée, exportez le projet. VIA génère un fichier JSON (similaire à `Annotation_train_set.json`).  
   - Veillez à bien nommer le fichier (ex. : `Annotation_train_set.json` ou `Annotation_val_set.json`, selon l’ensemble annoté).  
   - Conservez ce fichier dans le dossier `data/annotations_files` ou un emplacement de votre choix.

---

## Conversion du JSON pour YOLO

YOLO exige un format d’annotation différent du JSON produit par VIA. Afin de faciliter cette conversion, vous pouvez utiliser le **Notebook** dédié :

1. **Notebook de conversion**  
   - Dans le répertoire `scripts/Notebooks/`, ouvrez le fichier `conversion-YoloA_from_VggIA.ipynb`.  
   - Ce Notebook lit le fichier JSON produit par VIA et génère des fichiers d’annotation compatibles avec YOLO.  

2. **Fonctionnement (aperçu)**  
   - Le script extrait pour chaque image :  
     - le chemin de l’image,  
     - les coordonnées des bounding boxes,  
     - la catégorie associée (label).  
   - Il calcule ensuite les valeurs normalisées **(x_center, y_center, width, height)** attendues par YOLO.  
   - Enfin, il écrit un **fichier texte** (par image) contenant ces informations au format YOLO.  

3. **Organisation du jeu de données pour YOLO**  
   - Placez les fichiers texte d’annotations générés dans les sous-répertoires `train` et `val` de `data/dataset/`, en respectant la même structure que celle des images.  
   - Assurez-vous que la variable `path` ou `img_path` dans le Notebook correspond bien à l’emplacement de vos images.

4. **Vérification**  
   - Après la conversion, vérifiez que les fichiers .txt correspondent correctement aux images.  
   - Une simple vérification peut être faite via le Notebook de test.

---

## Fine-tuning du modèle YOLO

Une fois vos images annotées et converties :

1. **Préparation du répertoire**  
   - Assurez-vous que la structure `train` / `val` / `test` est cohérente dans `data/dataset/`.  
   - Vérifiez également le contenu du fichier `data.yaml` (dans `data/dataset/`) : il doit pointer vers les bons chemins et répertorier correctement les classes.

2. **Lancement de l’entraînement**  
   - Le Notebook `train_model.ipynb` (dans `scripts/Notebooks/`) vous permet de lancer un entraînement YOLO (version dépendante de vos besoins).  
   - Paramétrez vos hyperparamètres (batch size, epochs, etc.) avant de démarrer si vous le souhaitez.

3. **Évaluation**  
   - Utilisez directement les informations généré par l'entrainnement par Yolo pour évaluer la performance du modèle observer les métriques (mAP, Recall, Precision, etc.).  

3. **Visualisation**  
   - Utilisez le Notebook `test_model_video_fast.ipynb` pour visualiser le résultat de la prédiction du modele sur une vidéo.  

4. **Itérations et améliorations**  
   - Si les résultats ne sont pas satisfaisants, retournez à l’étape d’annotation ou ajustez votre data augmentation / hyperparamètres.  
   - Vous pouvez également affiner le partitionnement `train/val/test` pour obtenir de meilleures performances.

---


Pour toute question ou contribution, n’hésitez pas à ouvrir une **issue** ou à proposer une **pull request**.

