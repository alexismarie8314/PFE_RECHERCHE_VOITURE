# Projet de Fin d'Études : Optimisation et Sécurité des Trajets

## Description du Projet

Ce projet a pour objectif d'améliorer la sécurité et l'optimisation des trajets en milieu urbain grâce à l'intelligence artificielle. Il est divisé en deux modules principaux :

1. **Anticipation des accidents** : Un système basé sur la vision par ordinateur et l'apprentissage profond (deep learning) pour analyser les vidéos en temps réel et anticiper les accidents.
2. **Optimisation des trajets** : Un module de simulation pour fluidifier le trafic en utilisant la communication inter-véhicules, afin de contourner les perturbations (bouchons, accidents, etc.).

## Architecture du Projet

### 1. **Anticipation des Accidents**
Ce module utilise le modèle YOLO (You Only Look Once) pour détecter des situations dangereuses dans les vidéos. 
- **Dossier** : `anticipation_accident/`
- **Structure** :
  - `Dataset/CarCrash` : Ensemble de données pour l'entraînement du modèle YOLO.
  - `accident_anticipation` : Code et modèle YOLO optimisé pour analyser des vidéos image par image.
  - `reconnaissance_d_image` : Modèle YOLO pré-entraîné utilisé pour la reconnaissance des objets.

### 2. **Optimisation des Trajets**
Ce module étudie comment la communication inter-véhicules peut optimiser les temps de trajets dans un réseau routier urbain perturbé.
- **Dossier** : `optimisation_trajet/`
- **Structure** :
  - `Parsing_graph` : Scripts Python pour créer des graphes représentant les réseaux routiers de villes et effectuer des analyses.
  - `Sources` : Graphes routiers générés et résultats des simulations.

### 3. **Dossier d'Archivage**
Le dossier d'archivage contient l'ensemble des résultats obtenus durant les expérimentations ainsi que les documents détaillant les méthodologies employées.

- **Dossier** : `dossier_archivage/`
- **Contenu** :
  - Présentation du projet et de sa problématique.
  - Etats de l'arts.
  - Résultats des simulations pour les scénarios d'optimisation des trajets.
  - Analyses des performances du modèle YOLO pour l'anticipation des accidents.
  - Protocoles expérimentaux détaillés, plans d'expérience, interprétation des résultats.

## Méthodologie

### Anticipation des Accidents
1. **Dataset utilisé** :
   - **DFG Traffic Sign Dataset** : Pour la reconnaissance des panneaux de signalisation.
   - **Car Crash Dataset** : Pour l'entraînement à la détection des accidents.
2. **Approche technique** :
   - Modèle YOLOv8 pour la détection des objets (véhicules, piétons, panneaux).
   - Utilisation d'un réseau de neurones récurrents (RNN) pour évaluer la dangerosité des situations.

### Optimisation des Trajets
1. **Hypothèses étudiées** :
   - Impact de la communication entre véhicules sur les temps de trajets dans 4 scénarios : sans coopération, avec coopération partielle ou totale.
2. **Simulation** :
   - Algorithme de Dijkstra pour déterminer les chemins les plus courts dans des graphes représentant des villes.
   - Analyse comparative des performances sur des graphes de différentes tailles et niveaux de perturbation.

## Résultats Attendus
1. Une augmentation de la sécurité grâce à la détection précoce des situations dangereuses avec une précision supérieure à 60 % et un temps de réponse inférieur à 1 seconde.
2. Une réduction significative des temps de trajet grâce à la communication inter-véhicules dans les scénarios coopératifs.

## Prérequis

- **Langage de programmation** : Python
- **Bibliothèques nécessaires** :
  - `ultralytics` (YOLO)
  - `networkx` (graphes)
  - `matplotlib`, `numpy`, `pandas` (analyse de données)
- **Données** : Téléchargeables depuis [OpenStreetMap](https://www.openstreetmap.org/export).

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Heller-Theo/PFE_OPTIMISATION_TRAJET.git
   ```

## Utilisation

### Anticipation des Accidents
1. Téléchargez les datasets nécessaires et placez-les dans `Dataset/CarCrash`.
2. Lancez l'entraînement du modèle YOLO depuis le dossier `accident_anticipation`.

### Optimisation des Trajets
1. Placez les fichiers OSM téléchargés dans `Parsing_graph`.
2. Exécutez les scripts pour générer des graphes ou analyser les résultats dans `Sources`.

## Contributions
Projet réalisé par :
- Alexis MARIE, David MARCHÈS, Luca BANKOFSKI, Martial BROSTIN, Theo HELLER, Thomas MABILLE

## Références
- **YOLO Documentation** : [Ultralytics](https://docs.ultralytics.com)
- **Datasets** :
  - [DFG Traffic Sign Dataset](https://www.vicos.si/resources/dfg)
  - [Car Crash Dataset](https://github.com/Cogito2012/CarCrashDataset)
