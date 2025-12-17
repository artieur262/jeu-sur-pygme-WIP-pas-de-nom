class Comparator:
    EGALE = "="
    INFERIEUR = "<"
    SUPERIEUR = ">"
    INFERIEUR_OU_EGALE = "<="
    SUPERIEUR_OU_EGALE = ">="
    DIFERENT = "!="

    @staticmethod
    def compare(value1, value2, comparator: str) -> bool:
        
        if comparator == Comparator.EGALE:
            return value1 == value2
        elif comparator == Comparator.INFERIEUR:
            return value1 < value2
        elif comparator == Comparator.SUPERIEUR:
            return value1 > value2
        elif comparator == Comparator.INFERIEUR_OU_EGALE:
            return value1 <= value2
        elif comparator == Comparator.SUPERIEUR_OU_EGALE:
            return value1 >= value2
        elif comparator == Comparator.DIFERENT:
            return value1 != value2
        else:
            raise ValueError(f"Comparateur inconnu: {comparator}")


def main():
    a = "A"
    b = Comparator.EGALE
    c = "B"
    print(Comparator.compare(a, "A", b))  # True
    print(Comparator.compare(a, c, Comparator.DIFERENT))  # True
    print(b)
    print(type(b))


if __name__ == "__m