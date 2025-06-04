# 🚀 Airflow Project — Démonstration DAG avec Python et Bash

Ce projet est une démonstration fonctionnelle d’un pipeline **Apache Airflow 3.0.1**, contenant un DAG complet combinant des opérateurs Python, Bash et des branches conditionnelles. Il est conteneurisé via Docker pour une exécution rapide et isolée.

---

## 🗂 Structure du projet

```

📁 airflow\_project/
│── 📁 dags/
│   └── my\_first\_dag.py          # Définition du DAG principal
│
│── 📁 plugins/
│   └── utiles/functions.py      # Fonctions personnalisées (ex. transformations)
│
│── 🐳 Dockerfile                 # Image basée sur apache/airflow:3.0.1
│── 📄 requirements.txt          # Dépendances Python
│── 🐚 run.sh                    # Script pour build et exécuter le conteneur
│── 📘 README.md                 # Documentation du projet

```

---

## ⚙️ Contenu du DAG (`my_first_dag.py`)

Ce DAG s’exécute toutes les **30 secondes** (`schedule=timedelta(seconds=30)`) et démontre :

- Le passage de données entre tâches via **XCom**
- L’usage d’un **BranchPythonOperator**
- L’écriture dans un fichier via **BashOperator**
- La démonstration de la règle de déclenchement `TriggerRule.ONE_SUCCESS`

### 🔄 Logique du pipeline

```

first\_task → task\_bash → task\_random\_choice
↓
┌───────┴────────┐
↓                ↓
task\_1            task\_2
↓                ↓
└──────→ task\_goodbye

````

---

## 🐳 Utilisation avec Docker

### 1. 🔨 Build de l’image

```bash
bash run.sh
````

Ce script construit l’image Docker à partir du Dockerfile et monte le projet local dans le conteneur.

### 2. 🌐 Accès à l'interface Airflow

Une fois lancé, l’interface web Airflow est disponible ici :

👉 [http://localhost:8060](http://localhost:8060)

---

## 🧪 Dépendances Python

Les dépendances nécessaires sont listées dans `requirements.txt` :

```
apache-airflow
chromadb
```

---

## 🧼 Nettoyage

Pour arrêter et supprimer le conteneur Docker :

```bash
docker ps        # pour obtenir l’ID
docker stop <ID> && docker rm <ID>
```

---

## 📜 Licence

Projet pédagogique proposé par l'agence **Quera**
📍 16 rue Ernestine, 75018 Paris
📧 Contact : [kevin.duranty@quera.fr](mailto:kevin.duranty@quera.fr)
🧠 *La technologie au service du développement des activités humaines.*

