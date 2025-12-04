"""
ce module permet de remplacer des balises dans un text par une valeur
exemple :
remplace = {"{{chat}}":"pandi"}
transforme("Bonjour, j'ai trouver un chat et il avait le nom de {{chat}}.") ->
    -> "Bonjour, j'ai trouver un chat et il avait le nom de pandi.


oui je sais j'aurais pu faire une classe mais je voulais pas
car flemme et je pense pas que ça soit nécessaire
et en vrai avec python c'est un peu la même chose selon moi

a optimser un jour (surtout la fonction transforme)
"""

remplace: dict[str, any] = {}


def transforme(text: str) -> str:
    """cette fonction remplace les balises d'un texte par des valeurs.

    Args:
        text (str): est un text pouvant contenir des balises ou pas

    Returns:
        str: est le texte avec ses balises transformé
    """
    for cle, valeur in remplace.items():
        text = text.replace(cle, valeur)
    return text


def add_dico_and_balise(dico: dict):
    """ajoute les valeurs dans le dico des balises à remplacer et les entoures de {{}}.

    Args:
        dico (dict): dictionnaire avec les clefs et valeurs à ajouter
    """
    for clee, valeur in dico[1].items():
        remplace["{{" + clee + "}}"] = valeur


def add_dico(dico: dict):
    """ajoute les valeurs dans le dico des balises à remplacer.
    Args:
        dico (dict): dictionnaire avec les clefs et valeurs à ajouter
    """
    for clee, valeur in dico.items():
        remplace[clee] = valeur


def add_value(clee: str, valeur: any):
    """ajoute une valeur dans le dico des balises à remplacer.
    Args:
        clee (str): clef de la valeur à ajouter
        valeur (any): valeur à ajouter
    """
    remplace[clee] = valeur


def add_value_and_balise(clee: str, valeur: any):
    """ajoute une valeur dans le dico des balises à remplacer et entoure la clef de {{}}.
    Args:
        clee (str): clef de la valeur à ajouter
        valeur (any): valeur à ajouter
    """
    remplace["{{" + clee + "}}"] = valeur


def get_remplace():
    """renvoie le dico des balises à remplacer.
    Returns:
        dict[str, any]: dico des balises à remplacer
    """
    return remplace
