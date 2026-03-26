from py.objet.zone import Zone3D


def main1():
    zone0 = Zone3D([0, 0, 0], [10, 10, 10])
    zone1 = Zone3D([5, 0, 0], [10, 10, 10])
    zone2 = Zone3D([10, 0, 0], [10, 10, 10])
    zone3 = Zone3D([15, 0, 0], [10, 10, 10])
    zone_moins_3 = Zone3D([-15, 0, 0], [10, 10, 10])
    print("zone0 et zone1 :")
    print(zone0.collision_zone(zone1))
    print(zone0.contiens_zone(zone1))
    print(zone0.distance_entre_in_axe(zone1, 0))
    print("zone0 et zone2 :")
    print(zone0.collision_zone(zone2))
    print(zone0.contiens_zone(zone2))
    print(zone0.distance_entre_in_axe(zone2, 0))
    print("zone0 et zone3 :")
    print(zone0.collision_zone(zone3))
    print(zone0.contiens_zone(zone3))
    print(zone0.distance_entre_in_axe(zone3, 0))
    print("zone0 et zone_moins_3 :")
    print(zone0.collision_zone(zone_moins_3))
    print(zone0.contiens_zone(zone_moins_3))
    print(zone0.distance_entre_in_axe(zone_moins_3, 0))
    print("deplacer_in_axe :")
    # print("deplacement 1 :")
    # print(zone0.deplacer_in_axe(0, 5, [zone1, zone2, zone3, zone_moins_3]))
    # print(zone0.get_pos())
    # print("deplacement 2 :")
    # print(zone0.deplacer_in_axe(0, 5, [zone2, zone3, zone_moins_3]))
    # print(zone0.get_pos())
    print("deplacement 3 :")
    print(zone0.deplacer_in_axe(0, 25, set([zone3, zone_moins_3])))
    print(zone0.get_pos())


def main2():
    zone0 = Zone3D([0, 0, 0], [10, 10, 10])
    zone1 = Zone3D([15, 0, 0], [10, 10, 10])
    zone2 = Zone3D([30, 0, 0], [10, 10, 10])
    zone3 = Zone3D([45, 0, 0], [10, 10, 10])
    zone0.id = 0
    zone1.id = 1
    zone2.id = 2
    zone3.id = 3
    print("deplacer_in_axe :")
    print(zone0.deplacer_in_axe(0, 500, set([]), set([zone1, zone2, zone3])))
    print(zone0.get_pos())
    print(zone1.get_pos())
    print(zone2.get_pos())
    print(zone3.get_pos())


if __name__ == "__main__":
    # main1()
    main2()
