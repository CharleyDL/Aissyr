<!-- GETTING STARTED -->

## 🏁 Getting Started

**Protocole pour initialiser la base de données pour le projet NEO-AIssyr.**

Deux méthodes disponibles : _soit en local via **Docker** 🐳 ou via **Heroku** 🟪_

</br>

## 🖥️ Prérequis

**-- Commun au deux :**

- Installer Postgres
- Avoir ou créer un environnement virtuel avec le requirements du projet la commande suivante :

```bash
$ python -m venv <environment name>
$ cd <dossier du projet>
$ pip install -r requirements.txt
```

- Les données en local dans le dossier data (annotations, images, segments et neo_assyrian_info.json)
  > **⚠️** Si vous n'avez pas les données à la suite du git clone, vous pouvez les récupérer en lançant les **notebook_eda**

</br>

**-- 🐳 Pour une installation via Docker :**

- Installer Docker

</br>

**-- 🟪 Pour une installation via Heroku :**

- Un compte Heroku avec une Application et une Heroku Postgres
- Installer Heroku CLI _(cmd pour système Linux/OSX)_ :

```bash
brew tap heroku/brew && brew install heroku
```

</br>
</br>

## 🚀 Installation via Docker 🐳

1. Créer un fichier .env (dossier _/docker/postgres_) avec les variables d'environnements ci-dessous, pour la sécurité (**⚠️ ne pas git ce fichier**)

```
# - PATH
FOLDER_PATH = /Users/Projects/projet_NeoAIssyr/docker/postgres

# - POSTGRESQL
POSTGRES_DB = nom de la base
POSTGRES_USER = nom de votre user
POSTGRES_PASSWORD = votre mdp pour la base
POSTGRES_ROOT_PASSWORD = votre mdp root pour la base
POSTGRES_PORT = 5432 (ou autre port si besoin)

# - PGADMIN
PGADMIN_DEFAULT_EMAIL = votre mail pour connection
PGADMIN_DEFAULT_PASSWORD = votre mdp pour connection
```

2. Lancer le docker-compose (nécessite que docker soit ouvert). _Cela prend quelques minutes pour que les conteneurs se lancent et que la base de données s'initialise._
   ```bash
   $ docker-compose up -d
   ```
3. Ouvrir un navigateur web, et rendez vous à l'adresse :

   ```
   http://localhost:5050/
   ```

   Utiliser vos identifiant pour vous connecter à PGadmin _(PGADMIN_DEFAULT_EMAIL, PGADMIN_DEFAULT_PASSWORD)_

4. Dans l'interface créer une nouvelle connexion en appuyant sur **Add New Server**

   - **Les champs à renseigner :**
     - **Name (General) :** nom qui apparaîtra dans pgAdmin
     - **host (Connection) :** container_name de la base de données dans le docker-compose => ici **postgres_db**
     - **Username :** votre POSTGRES_USER
     - **Password :** votre POSTGRES_PASSWORD

5. Créer un fichier config.py (_/docker/postgres/script_), avec le template ci-dessous, pour y mettre les informations de connexion :

```python
import os


def get_db_config() -> dict:
    """
    Returns a dictionary containing database's informations,
    which are used by the following method : psycopg2.connect()
    """

    config = {
        ## -- Local Configuration -- ##
        "host" : "localhost",
        "database" : "<nom donner à la base sur pgAdmin>",
        "user" : <POSTGRES_USER>,
        "password" : <POSTGRES_PASSWORD> ,
        "port" : "5432"
    }

    return config

```

6. Lancer le script **clean_insert_data.py** et attendez que le processus soit fini :

```bash
$ python docker/postgres/script/clean_insert_data.py
```

7. Dans PgAdmin, copier-coller la requête 'request_labelisation_collection', dans l'outil SQL et utiliser la version 'local database'.  
   Faite ensuite la même chose avec 'request_label_view'.

</br>

> 🎉 La base est initialisée, vous pouvez dorénavant consulter les infos depuis la page web de pgAdmin

<p align="right">(<a href="#readme-top">back to top</a>)</p>

</br>
</br>

## 🚀 Installation via Heroku 🟪

1. Se connecter à son compte Heroku, si ce n'est pas fait créer une application et y ajouter un base de données Heroku Postgres

2. _Configurer Heroku CLI (si nécessaire)_

3. Créer un dataclips **INIT_DB** pour la base de données, utiliser le script **init_full_db.sql** (_/docker/postgres/_) en décommentant les parties :

```sql
/*
begin;
set transaction read write;
*/
...
/*COMMIT;*/
```

> Ceci a pour but d'initialiser la base de données avec les tables nécessaires. Attention aucune données n'est encore en base.

4. Créer un fichier config.py (_/docker/postgres/script_), avec le template ci-dessous, pour y mettre les informations de connexion d'Heroku :

```python
import os


def get_db_config() -> dict:
    """
    Returns a dictionary containing database's informations,
    which are used by the following method : psycopg2.connect()
    """

    config = {
        ## -- Heroku Configuration -- ##
        "host" : "",
        "database" : "",
        "user" : "",
        "password" : "",
        "port" : "5432"
    }

    return config

```

> **Information de connexion :**  
>  Sur la page de votre base de données :  
>  -> Settings -> Database Credentials -> View Credentials...

5. Lancer le script **clean_insert_data.py** et attendez que le processus soit fini :

```bash
$ python docker/postgres/script/clean_insert_data.py
```

6. Créer un dataclip (Heroku) pour copier-coller la requête 'request_labelisation_collection', puis un autre pour 'request_label_view'.
   Éxécuter les pour insérer les valeurs supplémentaires.

</br>

> 🎉 La base est initialisée, vous pouvez dorénavant consulter les infos depuis Heroku en utilisant le système de Dataclips pour écrire vos requêtes sql.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
