"""
test pour comparer differentes methodes pour savoir si un set est inclus dans un autre
conclusion : la deuxieme methode est plus rapide donc je suis mieulleur
que l'ia et on ne sera pas encore remplacé


"""

# a = set((1, 2, 3, 4))
# b = set((3, 4))


def test1():
    """fait par IA"""
    return a & b == b


def test2():
    """fait par moi"""
    return len(a & b) == len(b)


import random


a = [random.randint(1, 100) for _ in range(100000)]
b = [random.randint(1, 150) for _ in range(20000)]

a = set(a)
b = set(b)

if __name__ == "__main__":
    import time

    start = time.time()
    print(test1())
    print("test1:", time.time() - start)

    start = time.time()
    print(test2())
    print("test2:", time.time() - start)

    # start = time.time()
