# Analyseur de Statistiques de League of Legends

Cette application Flask récupère et affiche des statistiques de jeu pour des joueurs spécifiques de League of Legends, telles que les taux de victoire, les champions les plus joués, etc..
## Fonctionnalités

- Affichage des taux de victoire pour les joueurs spécifiés.
- Affichage des champions les plus joués et leurs taux de victoire.
- Affichage des champions le plus souvent bannis dans les parties de ces joueurs.
- Calcul et affichage du nombre moyen de balises de vision achetées et des pings moyens par match.

## Prérequis

- Python 3.6 ou supérieur.
- Clé API de Riot Games valide (à obtenir sur [Riot Developer Portal](https://developer.riotgames.com/)).

## Installation

1. Clonez ce dépôt sur votre machine locale.
2. Installez les dépendances Python nécessaires :

pip install -r requirements.txt

Pour démarrer l'application, exécutez la commande suivante dans votre terminal à la racine du projet :
python app.py

## Configuration
Pour changer les noms des invocateurs analysés, modifiez la liste summoner_names dans app.py.

## Licence
Distribué sous la licence MIT. Voir 'LICENSE' pour plus d'informations.
