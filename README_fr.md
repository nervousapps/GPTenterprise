<h1 align="center">
:office: GPTentreprise :zzz: :robot:
</h1>
<h1 align="center">
<img width="200" src="https://raw.githubusercontent.com/nervousapps/GPTenterprise/master/logo.png" alt="GPTenterprise">
</h1>

[![python](https://img.shields.io/badge/Python-3.7-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![openai](https://img.shields.io/badge/openai%20-GPT-yellowgreen)](https://www.openai.com)
[![Pylint](https://github.com/nervousapps/GPTenterprise/actions/workflows/pylint.yaml/badge.svg)](https://github.com/nervousapps/GPTenterprise/actions/workflows/pylint.yaml)
[![Pytest](https://github.com/nervousapps/GPTenterprise/actions/workflows/tests.yaml/badge.svg)](https://github.com/nervousapps/GPTenterprise/actions/workflows/tests.yaml)
[![Docs](https://github.com/nervousapps/GPTenterprise/actions/workflows/pdoc.yaml/badge.svg)](https://nervousapps.github.io/GPTenterprise/gpt_enterprise)

Première tentative d'émuler une entreprise avec OpenaAI GPT.

Il s'agit essentiellement d'un package Python émulant une entreprise. Il demande l'API OpenaAI et génère une séquence de tâches, chacune associée à un employé. Les employés sont générés automatiquement (le système invite GPT à dire quel employé être) :brain:.

## :night_with_stars: Résumé
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
- [:artificial_satellite: À propos de l'entreprise (par GPT)](#artificial_satellite-%C3%A0-propos-de-lentreprise-par-gpt)
- [:pinched_fingers: Exigences](#pinched_fingers-exigences)
- [:surfing_woman: Installation](#surfing_woman-installation)
- [:unicorn: Configuration de la clé OpenAI](#unicorn-configuration-de-la-cl%C3%A9-openai)
- [:point_right: Démarrage rapide v1](#point_right-d%C3%A9marrage-rapide-v1)
- [:books: Documentation](#books-documentation)
  - [:label: Variables d'environnement (fichier de configuration)](#label-variables-denvironnement-fichier-de-configuration)
- [:roller_coaster: Aller plus loin](#roller_coaster-aller-plus-loin)
- [:white_check_mark: Tests](#white_check_mark-tests)
- [:recycle: Formatter](#recycle-formatter)
- [:raccoon: Divers](#raccoon-divers)
  - [:older_woman: Démarrage rapide POC](#older_woman-d%C3%A9marrage-rapide-poc)
- [:carousel_horse: Avertissements](#carousel_horse-avertissements)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## :artificial_satellite: À propos de l'entreprise (par GPT)
<p>Notre entreprise innovante utilise une technologie de pointe d'intelligence artificielle pour améliorer les produits et services. Nos employés sont des instances d'AI créées avec le puissant modèle de langage GPT qui peuvent remplir divers rôles tels que des ingénieurs, des concepteurs et même des marketeurs. Cela nous permet de développer des produits plus rapidement et plus efficacement que les entreprises traditionnelles tout en offrant une expérience unique à nos clients.</p>
		
		
<p>Nos employés d'AI sont équipés des dernières technologies et apprennent constamment et s'adaptent à de nouvelles situations. Cela nous permet d'être plus agiles et réactifs aux changements de marché, en veillant à ce que nos produits et services soient toujours à la pointe de l'innovation.</p>
		
<p>Si vous êtes intéressé par l'expérience de la technologie AI de l'avenir, découvrez notre produit.</p>

<p>Avis de non-responsabilité : nos employés d'AI ne sont pas destinés à remplacer les travailleurs humains et sont conçus pour être utilisés en complément des équipes humaines. Nous croyons à la puissance de la créativité et de l'intelligence humaines combinées à une technologie avancée.</p>

## :pinched_fingers: Exigences

- Python 3.7 ou plus récent

- [Clé Open API](https://platform.openai.com/account/api-keys)

## :surfing_woman: Installation
1 - Clonez ce dépôt
```bash
git clone https://github.com/nervousapps/GPTenterprise.git
```

2 - Allez dans le répertoire de dépôt
```bash
cd GPTenterprise
```

3 - Il est recommandé d'utiliser un environnement virtuel Python, pour en créer un, dans votre terminal :
```bash
python3 -m venv gptentreprise
```
Et activez-le
```bash
source ./gptentreprise/bin/activate
```

4 - Installez le package GPTentreprise et ses dépendances en exécutant :
```bash
pip install ./python
```

## :unicorn: Configuration de la clé OpenAI
- Remplissez openai_key.txt.template avec votre clé Openai et renommez-le en openai_key.txt. Ou en créer un nouveau avec :
```bash
nano ./openai_key.txt
```


## :point_right: Démarrage rapide v1
Pour voir un exemple de ce que l'on peut faire avec l'idée de GPTentreprise :

1 - Ajustez le fichier de configuration pour donner des directives au :superhero_man: PDG (et d'autres paramètres si vous le souhaitez, mais les valeurs par défaut devraient suffire)

```bash
nano ./config
```

2 - Exécutez l'entreprise

```bash
GPTentreprise ./config
```

Ensuite, l'entreprise sera créée avec vos directives et un manager sera embauché. Il fera de son mieux pour atteindre les directives.
Le manager établira un plan, avec tous les employés à embaucher et les séquences de tâches qui seront exécutées pour produire le résultat souhaité.

## :books: Documentation

[Documentation HTML ici](https://nervousapps.github.io/GPTenterprise/gpt_enterprise).

Documentation générée avec [PDOC](https://pdoc.dev/)

Une entreprise est composée d'un manager (un seul pour l'instant) et d'employés.
Au début, le PDG créera l'entreprise en donnant ses directives au manager.
Le manager créera ensuite une séquence de tâches, chacune associée à un employé.
Chaque employé sera embauché par le manager pour ses compétences. Un employé est défini comme une invite système, générée automatiquement par le manager, qui décrit ses compétences.

:warning:L'invite du gestionnaire définit la structure objet pour les employés, les tâches et l'objet global. Ces structures ne doivent pas être modifiées car elles sont utilisées dans le code.

:red_haired_woman: Structure de l'employé
```python
{
    "name": "Employee's name",
    "role_name": "Employee's role name",
    "role": "Employee's role (system prompt)"
    "creativity": 1.0
    "emoji": "Emoji code"
}
```
Le nom et le nom de rôle doivent être uniques.

:bookmark: Structure de tâche
```python
{
    "task_name":
    "employee":
    "todo":
    "type":
    "requirements": '("yes" or "no")'
}
```
À chaque tâche, le gestionnaire ajoutera un champ de résultat avec le travail de l'employé.

:newspaper_roll: Structure des plans
```python
{
    "employees": [employee1, employee2],
    "tasks": [task1, task2],
}
```

Le produit final peut être trouvé dans le champ final_product de l'objet json contenu dans le fichier "production_<nom_de_l'entreprise>.json" dans le répertoire de sortie spécifié.


### :label: Variables d'environnement (fichier de configuration)
| nom env                       | description     | valeur par défaut      |
| -------------------------------| ----------------| -------------------|
| COMPANY_NAME                   | Nom de l'entreprise                                                       | GPTenterprise   | 
| KEYFILE                        | Chemin d'accès au fichier keyfile.txt de OpenAI                                            | ./openai_key.txt|
| OUTPUT_DIRECTORY               | Répertoire de sortie                                                      | ./generated/v2  |
| MANAGER_RETRY                  | Combien de fois le gestionnaire réessayera de faire les plans en cas d'échec          | 1               |
| CUSTOM_MANAGER_PROMPTS_PATH    | Fournit une invite de gestionnaire personnalisée (veillez à conserver les définitions de structure d'objets) | ""              |
| CEO_GUIDELINES                 | "En tant que PDG, je veux ..."                                         | "En tant que PDG, je veux ..." |
| INTERACTIVE                    | Attendez l'entrée de l'utilisateur (basique pour l'instant)                                        | "non" |

## :roller_coaster: Aller plus loin
- Repenser l'invite du gestionnaire
- Interactions améliorées des employés
- Opérations asynchrones
- Entreprise de plusieurs gestionnaires
- Garder les réponses précédentes en mémoire (peut-être utiliser https://github.com/acheong08/ChatGPT)
- Recherche sur Internet (en Python seulement pour éviter d'utiliser le jeton OpenAI)

## :white_check_mark: Tests
1 - Installer les exigences de test
```bash
pip install -r ./python/requirements-tests.txt
```

2 - Exécuter les tests
```bash
pytest
```

## :recycle: Formateur

[BLACK](https://pypi.org/project/black/)


## :raccoon: Divers
### :older_woman: POC de démarrage rapide

Pour voir un exemple de ce qui peut être fait avec l'idée de GPTenterprise, utilisons webgpt.py

WebGPT est une entreprise pilotée par l'IA qui développe des sites Web pour ses clients.

Il est composé de plusieurs employés GPT (invites) :

- :writing_hand: un prompteur de sujet, qui est responsable de la formulation de sujets.

- :camera_flash: un prompteur de dall-e, qui est responsable de la génération de invites à injecter dans dall-e pour la génération d'images sur le sujet précédemment généré.

- :desktop_computer: un développeur Web, qui est responsable de la programmation du site Web sur le sujet et les images précédemment générés.

- :superhero_man: un PDG (vous), qui est responsable de piloter tout cela et de diriger l'entreprise.

Pour exécuter l'entreprise, veuillez faire :
```bash
python ./examples/webgpt.py
```

## :carousel_horse: Avertissements
Il ne s'agit pas d'un produit officiel d'OpenAI. Il s'agit d'un projet personnel et il n'est affilié d'aucune manière à OpenAI.