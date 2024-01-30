"""cat """


class Logique:
    """ce block logique permet de faire des opération logique"""

    def __init__(self, id_activation: list[int], id_sorti: int, type_: str):
        self.id_activation = set(id_activation)
        self.id_sorti = id_sorti
        self.active = False
        self.type = type_  # "and"  | "or" | "xor"

    def activation(self, set_activation: set):
        """permet d'activé une id d'activation"""
        # print(
        #     self.id_activation,
        #     len(self.id_activation & set_activation) == len(self.id_activation),
        # )
        if self.type == "and" and len(self.id_activation & set_activation) == len(
            self.id_activation
        ):
            self.active = True
        elif self.type == "or" and self.id_activation & set_activation:
            self.active = True
        elif (
            self.type == "xor"
            and self.id_activation & set_activation
            and len(self.id_activation & set_activation) != len(self.id_activation)
        ):
            self.active = True

    def activate(self, set_activation: set):
        """active les objets avec l'id de sorti"""
        if self.active:
            set_activation.add(self.id_sorti)

    def actualise(self):
        """actualise l'activation du block logique"""
        self.active = False

    def convert_save(self) -> dict:
        """conveti sous un forma on il pourra entre rucupérer"""
        sorti = {
            "type": "logique",
            "entre": list(self.id_activation),
            "sorti": self.id_sorti,
            "mode": self.type,
        }
        # print(sorti)
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        """permet de convertir un dictionaire en objet"""
        return Logique(dic["entre"], dic["sorti"], dic["mode"])


class LogiqueNot:
    """ce block logique permet de faire une opération logique not"""

    def __init__(self, id_activation: int, id_sorti: int):
        self.id_activation = id_activation
        self.id_sorti = id_sorti
        self.active = True

    def activation(self, set_activation: set):
        """permet d'activé une id d'activation"""
        if self.id_activation in set_activation:
            self.active = False

    def actualise(self):
        """actualise l'activation du block logique"""
        self.active = True

    def activate(self, set_activation: set):
        """active les objets avec l'id de sorti"""
        if self.active:
            set_activation.add(self.id_sorti)

    def convert_save(self) -> dict:
        """conveti sous un forma on il pourra entre rucupérer"""
        sorti = {"type": "not", "entre": self.id_activation, "sorti": self.id_sorti}
        # print(sorti)
        return sorti

    @staticmethod
    def convert_load(dic: dict):
        """permet de convertir un dictionaire en objet"""
        return LogiqueNot(dic["entre"], dic["sorti"])


class LogiqueTimer:
    """ce block logique permet de faire un timer"""

    def __init__(self, crono, id_activation, id_sorti) -> None:
        self.crono = crono
        self.list_timer = set()
        self.active = False
        self.id_activation = id_activation
        self.id_sorti = id_sorti

    def actualise(self):
        """actualise le timer"""
        self.list_timer = {x - 1 for x in self.list_timer}
        if 0 in self.list_timer:
            self.active = True
            self.list_timer.remove(0)
        else:
            self.active = False

    def convert_save(self) -> dict:
        """conveti sous un forma on il pourra entre rucupérer"""
        sorti = {
            "type": "timer",
            "entre": self.id_activation,
            "sorti": self.id_sorti,
            "crono": self.crono,
        }
        return sorti

    def activation(self, set_activation: set):
        """permet d'activé une id d'activation"""
        if self.id_activation in set_activation:
            self.list_timer.add(self.crono)

    def activate(self, set_activation: set):
        """active les objets avec l'id de sorti"""
        if self.active:
            set_activation.add(self.id_sorti)

    @staticmethod
    def convert_load(dic: dict):
        """permet de convertir un dictionaire en objet"""
        return LogiqueTimer(dic["crono"], dic["entre"], dic["sorti"])


class LogiqueChangement:
    """ce block logique permet de faire un check de changement"""

    def __init__(self, id_activation, id_sorti) -> None:
        self.dernier_etat = None
        self.active = False
        self.id_activation = id_activation
        self.id_sorti = id_sorti

    def actualise(self):
        """actualise la derniere activation"""
        self.active = False

    def activation(self, set_activation: set):
        """permet d'activé une id d'activation"""
        if self.dernier_etat is None:
            # print("cat1")
            self.dernier_etat = self.id_activation in set_activation
        elif (self.id_activation in set_activation) != self.dernier_etat:
            # print("cat2", self.dernier_etat, self.id_activation in set_activation)
            self.dernier_etat = self.id_activation in set_activation
            self.active = True

    def activate(self, set_activation: set):
        """active les objets avec l'id de sorti"""
        if self.active:
            set_activation.add(self.id_sorti)

    def convert_save(self) -> dict:
        """conveti sous un forma on il pourra entre rucupérer"""
        sorti = {
            "type": "changement",
            "entre": self.id_activation,
            "sorti": self.id_sorti,
        }
        return sorti

    @staticmethod
    def convert_load(obj: dict):
        """permet de convertir un dictionaire en objet"""
        return LogiqueChangement(obj["entre"], obj["sorti"])
