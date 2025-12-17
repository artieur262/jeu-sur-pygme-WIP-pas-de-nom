class Comparator:
    EGALE = "="
    INFERIOR = "<"
    SUPERIOR = ">"
    INFERIOR_OU_IGUALE = "<="
    SUPERIOR_OU_IGUALE = ">="
    DIFERENTE = "!="

    @staticmethod
    def compare(value1, value2, comparator: str) -> bool:
        if comparator == Comparator.EGALE:
            return value1 == value2
        elif comparator == Comparator.INFERIOR:
            return value1 < value2
        elif comparator == Comparator.SUPERIOR:
            return value1 > value2
        elif comparator == Comparator.INFERIOR_OU_IGUALE:
            return value1 <= value2
        elif comparator == Comparator.SUPERIOR_OU_IGUALE:
            return value1 >= value2
        elif comparator == Comparator.DIFERENTE:
            return value1 != value2
        else:
            raise ValueError(f"Comparador desconhecido: {comparator}")


def main():
    a = "A"
    b = Comparator.EGALE
    c = "B"
    print(Comparator.compare(a, "A", b))  # True
    print(Comparator.compare(a, c, Comparator.DIFERENTE))  # True
    print(b)
    print(type(b))


if __name__ == "__main__":
    main()
