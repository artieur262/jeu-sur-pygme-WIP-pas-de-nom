"""cette class permet de comparer deux valeurs selon un comparateur donné"""


class Operateur:
    """cette class permet de comparer deux valeurs selon un comparateur donné

    Attributes:
        EGALE (str): comparateur pour egalité
        INFERIEUR (str): comparateur pour inferieur
        SUPERIEUR (str): comparateur pour superieur
        INFERIEUR_OU_EGALE (str): comparateur pour inferieur ou
        SUPERIEUR_OU_EGALE (str): comparateur pour superieur ou egal
        DIFERENT (str): comparateur pour different

    Methods:
        compare(value1, value2, comparator: str) -> bool:
            compare deux valeurs selon le comparateur donné

    """

    EGALE = "="
    INFERIEUR = "<"
    SUPERIEUR = ">"
    INFERIEUR_OU_EGALE = "<="
    SUPERIEUR_OU_EGALE = ">="
    DIFERENT = "!="
    PLUS = "+"
    MOINS = "-"
    FOIS = "*"
    DIVISE = "/"
    PUISSANCE = "**"
    MODULO = "%"

    @staticmethod
    def compare(value1, value2, comparator: str) -> bool:
        """compare deux valeurs selon le comparateur donné"""
        match comparator:
            case Operateur.EGALE:
                return value1 == value2
            case Operateur.INFERIEUR:
                return value1 < value2
            case Operateur.SUPERIEUR:
                return value1 > value2
            case Operateur.INFERIEUR_OU_EGALE:
                return value1 <= value2
            case Operateur.SUPERIEUR_OU_EGALE:
                return value1 >= value2
            case Operateur.DIFERENT:
                return value1 != value2
            case _:
                raise ValueError(f"Comparateur inconnu: {comparator}")

    @staticmethod
    def is_arithmetic_operator(operator: str) -> bool:
        """verifie si un symbole est un operateur arithmetique"""
        return operator in {
            Operateur.PLUS,
            Operateur.MOINS,
            Operateur.FOIS,
            Operateur.DIVISE,
            Operateur.PUISSANCE,
            Operateur.MODULO,
        }

    @staticmethod
    def is_comparison_operator(operator: str) -> bool:
        """verifie si un symbole est un operateur de comparaison"""
        return operator in {
            Operateur.EGALE,
            Operateur.INFERIEUR,
            Operateur.SUPERIEUR,
            Operateur.INFERIEUR_OU_EGALE,
            Operateur.SUPERIEUR_OU_EGALE,
            Operateur.DIFERENT,
        }

    @staticmethod
    def is_operator(operator: str) -> bool:
        """verifie si un symbole est un operateur"""
        return Operateur.is_arithmetic_operator(
            operator
        ) or Operateur.is_comparison_operator(operator)

    @staticmethod
    def operate(value1, value2, operator: str) -> int:
        """effectue une operation arithmetique entre deux valeurs"""
        match operator:
            case Operateur.PLUS:
                return value1 + value2
            case Operateur.MOINS:
                return value1 - value2
            case Operateur.FOIS:
                return value1 * value2
            case Operateur.DIVISE:
                return value1 // value2
            case Operateur.PUISSANCE:
                return value1**value2
            case Operateur.MODULO:
                return value1 % value2
            case Operateur.INFERIEUR, Operateur.INFERIEUR_OU_EGALE:
                return min(value1, value2)
            case Operateur.SUPERIEUR, Operateur.SUPERIEUR_OU_EGALE:
                return max(value1, value2)
            case _:
                raise ValueError(f"Operateur inconnu: {operator}")
