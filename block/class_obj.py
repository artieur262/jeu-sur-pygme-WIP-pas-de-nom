"""est module de class"""

#  pylint: disable=unused-import wildcard-import unused-wildcard-import
# from typing import Any

# # from typing
# import traceback


from .class_block import *
from .block_activable import PlateformeMouvante, BlockLumiere
from .block_special import (
    BlockCore,
    TunelDimensionelBrigitte,
    RedimentioneurPlayer,
    Graviteur,
)
from .block_logique import LogiqueNot, Logique, LogiqueTimer, LogiqueChangement
from .block_activateur import Interupteur, ZoneActive
from .block_texte import BlockTexte
from .playeur import Playeur

# traceback.print_stack()


# class BlocGlissant(Pave):
#     def cat(self):
#         pass


def genere_obj(
    liste: list[dict],
) -> dict[
    str,
    list[
        Block
        | PlateformeMouvante
        | Playeur
        | Interupteur
        | ZoneActive
        | BlockLumiere
        | BlockTexte
        | BlockCore
        | TunelDimensionelBrigitte
        | Logique
        | LogiqueNot
        | LogiqueTimer
        | LogiqueChangement
    ],
]:
    """genere les objets à partir d'une liste de dictionaire"""
    sorti = {
        "block": [],
        "playeur": [],
        "texte": [],
        #
        "interupteur": [],
        "zone_acitve": [],
        "plaforme": [],
        "lumière": [],
        #
        "core": [],
        "tunel_dimensionel": [],
        "redimentioneur": [],
        "graviteur": [],
        #
        "logique": [],
    }
    for obj in liste:
        # print(obj)
        if obj["type"] == "block":
            sorti["block"].append(Block.convert_load(obj))
        elif obj["type"] == "texte":
            sorti["texte"].append(BlockTexte.convert_load(obj))
        elif obj["type"] == "player":
            sorti["playeur"].append(Playeur.convert_load(obj))

        elif obj["type"] == "interupteur":
            sorti["interupteur"].append(Interupteur.convert_load(obj))
        elif obj["type"] == "zone":
            sorti["zone_acitve"].append(ZoneActive.convert_load(obj))

        elif obj["type"] == "lumière":
            sorti["lumière"].append(BlockLumiere.convert_load(obj))
        elif obj["type"] == "plaforme":
            sorti["plaforme"].append(PlateformeMouvante.convert_load(obj))

        elif obj["type"] == "core":
            sorti["core"].append(BlockCore.convert_load(obj))
        elif obj["type"] == "tunel_dimensionel":
            sorti["tunel_dimensionel"].append(
                TunelDimensionelBrigitte.convert_load(obj)
            )
        elif obj["type"] == "redimentioneur":
            sorti["redimentioneur"].append(RedimentioneurPlayer.convert_load(obj))
        elif obj["type"] == "graviteur":
            sorti["graviteur"].append(Graviteur.convert_load(obj))

        elif obj["type"] == "logique":
            sorti["logique"].append(Logique.convert_load(obj))
        elif obj["type"] == "not":
            sorti["logique"].append(LogiqueNot.convert_load(obj))
        elif obj["type"] == "timer":
            sorti["logique"].append(LogiqueTimer.convert_load(obj))
        elif obj["type"] == "changement":
            sorti["logique"].append(LogiqueChangement.convert_load(obj))
    return sorti
