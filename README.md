# Projet_ACV_pushup
#  Compteur de Pompes avec MediaPipe & OpenCV

Ce projet utilise **MediaPipe** et **OpenCV** pour détecter et compter automatiquement les **pompes** (push-ups) à partir d'une webcam.  
La logique de comptage se base sur la **position verticale des épaules et/ou des coudes** pour détecter une descente et une remontée complètes.

---

##  Fonctionnalités

- Détection en temps réel avec webcam.
- Suivi du corps avec MediaPipe Pose.
- Comptage automatique des pompes.
- Affichage du nombre de pompes à l’écran.

---

##  Installation

### 1. Cloner le projet
```bash
git git@github.com:DidiCi/Projet_ACV_pushup.git
cd pushup-counter-mediapipe
####2. Créer un environnement 
#  3. Installer mediapipe 
pushup-counter-mediapipe/
├── pushup_counter.py         # Code principal
├── utils.py                  # Fonctions utilitaires (classify_up_down, etc.)
├── requirements.txt
└── README.md
