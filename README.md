# BrickSearch : Recherche de pièces LEGO

Bienvenue dans ce dépôt GitHub dédié au projet **Recherche de pièces LEGO**. Ce document fournit une première vue d’ensemble du contexte, de la problématique ainsi que de l’objectif de ce projet.

## Contexte
Les passionnés de LEGO connaissent souvent la difficulté de retrouver une pièce précise parmi plusieurs centaines de briques mélangées. Que vous soyez un collectionneur chevronné ou un simple amateur, la recherche d’une brique en particulier peut rapidement se révéler chronophage. L’idée derrière ce projet est de s’appuyer sur des outils automatisés, de la documentation existante et une base de données de pièces pour accélérer et faciliter l’identification, puis la localisation de la brique souhaitée.

## Problématique
- **Complexité des références** : LEGO propose de très nombreuses pièces, chacune possédant des numéros d’identification, des variations de couleurs.
- **Organisation des inventaires** : LMa recherche efficace d’une pièce demeure un défi, surtout quand les quantités deviennent importantes.
- **Gain de temps et fiabilité** : L’identification manuelle de chaque pièce peut prendre un temps considérable.

## Objectif
Le principal objectif est de développer un outil ou un ensemble de scripts permettant :
1. D’identifier rapidement une pièce LEGO à partir d’une photo, d'une vidéo.
2. De fournir à l’utilisateur des informations pertinentes sur la pièce recherchée (numéro, nom exact, disponibilité, prix indicatif, etc.).

En centralisant et en automatisant ces tâches, le projet **Recherche de pièces LEGO** vise à rendre la recherche plus rapide et plus précise, que ce soit pour des utilisateurs occasionnels ou des utilisateurs avertis.

Voici une proposition de **complément** au README existant. Le texte original reste inchangé ; seul du contenu additionnel est proposé pour présenter la structure des répertoires et expliquer le rôle de certains fichiers clés identifiés dans le projet.

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
│   │   └── train
│   │   └── val
│   ├── model
│   └── raw
├── docs
├── ouputs
│   ├── images_annotees
│   ├── json_annotation_img
│   └── output_models
├── scripts
│   └── Notebooks
│       ├── conversion-YoloA_from_VggIA.ipynb
│       ├── test_model.ipynb
│       └── train_model.ipynb
├── tools
│   └── via-2.0.12
├── LICENSE
└── README.md


```

- **`data/`** : Contient les jeux de données (images brutes, labels, fichiers d’annotations).  
  - **`annotations_files/Annotation_train_set.json`** : Exemple de fichier d’annotations généré via le VGG Image Annotator (VIA).  
  - **`dataset/`** : Répertoire principal pour l’entraînement, la validation et le test (sous-répertoires `train`, `val` et `test`).  
  - **`model/`** : Stocke les poids pré-entraînés .  
  - **`raw/`** : Fichiers d’images brutes, non annotées.

- **`docs/`** : Rassemble la documentation associée au projet (ex. : Objectif, Etapes, guides, fichiers bureautiques).

- **`ouputs/`** : Contient les résultats (images annotées, JSON final, rapports de performance et poids finaux du modèle).

- **`scripts/Notebooks/`** :  
  - **`conversion-YoloA_from_VggIA.ipynb`** : Notebook pour convertir ou adapter les annotations du format VGG Image Annotator (VIA) en un format exploitable par YOLO ou inversement.  
  - **`test_model.ipynb`** : Permet de tester le modèle entraîné sur un ensemble de données de test.  
  - **`train_model.ipynb`** : Lance le processus d’entraînement du modèle YOLO sur les images annotées.

- **`tools/via-2.0.12/`** : Fichiers relatifs à l’outil VGG Image Annotator (VIA), utilisé pour la création et la gestion des annotations.

- **Fichiers de configuration** :  
  - **`LICENSE`** : Conditions de licence et de redistribution du projet.  

---
