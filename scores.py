import typing

from .score import Score

import yaml

# Chemin du fichier YAML
file_path = "snake_scores.yml"

# Charger les données existantes du fichier YAML
def load_yaml(file_path):
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            return data if data else []
    except FileNotFoundError:
        # Si le fichier n'existe pas, retourner une liste vide
        return []

# Sauvegarder les données dans le fichier YAML
def save_yaml(file_path, data):
    with open(file_path, "w") as file:
        yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)

# Ajouter un nouveau joueur avec son score
def add_player(file_path, player_name, score):
    data = load_yaml(file_path)
    # Vérifier si le joueur existe déjà
    if any(player["name"] == player_name for player in data):
        print(f"Le joueur '{player_name}' existe déjà.")
    else:
        # Ajouter le nouveau joueur
        data.append({"name": player_name, "score": score})
        save_yaml(file_path, data)
        print(f"Le joueur '{player_name}' a été ajouté avec un score de {score}.")

# Lire le fichier YAML et retourner un dictionnaire Python



class Scores :
    """Contains instances of scores."""

    def __init__(self, max_scores : int, scores : list[Score]) -> None :
        """Define the scores."""
        self._max_scores=max_scores
        self._scores=sorted(scores, reverse = True)[:max_scores]


    @classmethod
    def default(cls, max_scores):
        try:
            with open("snake_scores.yml", "r") as file:
                data = yaml.safe_load(file)  # Charger les données YAML
        except FileNotFoundError:
            data = []  # Valeurs par défaut si le fichier n'existe pas

    # Vérifier que les données sont une liste de dictionnaires
        if not isinstance(data, list) or not all(isinstance(player, dict) for player in data):
            raise TypeError(f"Le fichier YAML doit contenir une liste de dictionnaires : {data}")

    # Générer le dictionnaire des scores
        result = {player["name"]: player["score"] for player in data}

        return cls(
        max_scores,
        [Score(score=result.get("Joe", 0), name="Joe"),
                Score(score=result.get("Jack", 8), name="Jack"),
                Score(score=result.get("Averell", 0), name="Averell"),
                Score(score=result.get("William", 6), name="William"),
            ],
            )


    def __iter__(self) -> typing.Iterator[Score]:
        """Iterate on the list of scores."""
        return iter(self._scores)


    def is_highscore(self, score_player : int) -> bool :
        """Define the case highscore."""
        return len(self._scores)<self._max_scores or score_player > self._scores[-1]

    def add_score(self, score_player: Score) -> None:
        """Add a score and sort the list."""
        if self.is_highscore(score_player.score):
            if len(self._scores)>=self._max_scores :
                self._scores.pop()
            self._scores.append(score_player)
            self._scores.sort(reverse=True)













