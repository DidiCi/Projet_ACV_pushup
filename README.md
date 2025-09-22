# 💪 Projet_ACV_pushup
## 🤖 Compteur de Pompes avec MediaPipe & OpenCV

Ce projet utilise **MediaPipe** et **OpenCV** pour détecter et compter automatiquement les **pompes** (push-ups) à partir d'une webcam.  
La logique de comptage se base sur la **position verticale des épaules et/ou des coudes** pour détecter une descente et une remontée complètes.

---

## ✨ Fonctionnalités

- 🎥 Détection en temps réel avec webcam.
- 🧍 Suivi du corps avec MediaPipe Pose.
- 🧠 Comptage automatique des pompes.
- 📊 Affichage du nombre de pompes à l’écran.

---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone git@github.com:DidiCi/Projet_ACV_pushup.git
cd Projet_ACV_pushup
```

### 2. Créer un environnement
```bash
conda env create -f envirornment.yml
conda activate tf-env
```

### 3. Exécuter le programme
```bash
python main.py
```

---

## 📝 Auteurs

- 👤 Jip Wulffelé
- 👤 Diletta Ciardo
- 👤 Jamila Obeid

🎓 Réalisé dans le cadre du module ACV au sein du Campus Numérique dans les Alpes