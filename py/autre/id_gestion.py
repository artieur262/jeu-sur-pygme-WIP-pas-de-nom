"""Gestion des id uniques"""


global derniere_id #pylint: disable=global-statement, redefined-outer-name, global-at-module-level
all_id = {0}
derniere_id = 0


def genere_id() -> int:
    """Génère un id unique"""
    global derniere_id #pylint: disable=global-statement
    derniere_id += 1
    while derniere_id in all_id:
        derniere_id += 1
    ajoute_id(derniere_id)
    return derniere_id


def ajoute_id(id_):
    """Ajoute un id"""
    all_id.add(id_)


def supprime_id(id_):
    """Supprime un id"""
    all_id.remove(id_)
