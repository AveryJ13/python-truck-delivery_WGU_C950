# Avery Johnson WGU Delivery Application
# Student ID: 011430854

import csv
import datetime
from CreateHashTable import CreateHashTable
from Truck import Truck
from Package import Package

# function to open csv file and return it in the appropriate list format
def read_csv(path):
    with open(path) as f:
        return list(csv.reader(f))

# function above used to open the csv files. These are set to list(csv.reader(f)) on line 13
addresses = read_csv("csv/address.csv")
distances = read_csv("csv/distance.csv")
packages_raw = read_csv("csv/package.csv")

# trucks are manually loaded with the proper package groupings, the hard coded string is the starting hub
truck1 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
               [1,13,14,15,16,19,20,27,29,30,31,34,37,40])
truck2 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20),
               [2,3,4,5,9,18,26,28,32,35,36,38])
truck3 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
               [6,7,8,10,11,12,17,21,22,23,24,25,33,39])

# custom hashtable is filled in with the contents of the packages
def import_packages(path, table):
    with open(path) as f:
        rows = csv.reader(f)
        next(rows)
        for r in rows:
            pid = int(r[0])
            pkg = Package(pid, r[1], r[2], r[3], r[4], r[5], r[6], r[7],
                          "HUB", None, None)
            table.insert(pid, pkg)

# helper function to return the correct address for comparison in the algorithm later
def locate_address(street):
    for item in addresses:
        if street in item[2]:
            return int(item[0])

# returns the distance table entry between two locations. Since only half of the chart is filled in,
# the if statement provided checks the opposite side of the table if there's an empty value
def lookup_distance(a, b):
    d = distances[a][b]
    if d == "":
        d = distances[b][a]
    return float(d)

table = CreateHashTable(40)
import_packages("csv/package.csv", table)

# nearest neighbor algorithm
def run_route(truck):
    pending = [table.search(pid) for pid in truck.packages]
    truck.packages.clear()

    # priority queue is to ensure that all packages are delivered before 10:30 in these packageIDs
    priority_queue = {1, 13, 14, 16, 20, 25, 29, 30, 31, 34, 37, 40}
    first_pkg = None
    priority = []
    normal = []

    # 15 has an earlier deadline of 9:00 and is therefore delivered first
    for p in pending:
        if p.ID == 15:
            first_pkg = p
        elif p.ID in priority_queue:
            priority.append(p)
        else:
            normal.append(p)

    # first package delivered
    if first_pkg:
        d = lookup_distance(locate_address(truck.location),
                            locate_address(first_pkg.street))

        truck.miles += d
        truck.location = first_pkg.street
        truck.time += datetime.timedelta(hours=d / 18)
        first_pkg.delivery = truck.time
        first_pkg.departure = truck.departure
        truck.packages.append(first_pkg.ID)

    # priority packages delivered with nearest neighbor
    while priority:
        best = None
        best_dist = float("inf")
        for pkg in priority:
            d = lookup_distance(locate_address(truck.location),
                                locate_address(pkg.street))
            if d < best_dist:
                best_dist = d
                best = pkg

        truck.packages.append(best.ID)
        priority.remove(best)
        truck.miles += best_dist
        truck.location = best.street
        truck.time += datetime.timedelta(hours=best_dist / 18)
        best.delivery = truck.time
        best.departure = truck.departure

    pending = normal

    # loops through remaining pending packages. ends when pending is empty.
    while pending:
        best = None
        best_dist = float("inf")

        # nearest neighbor is below, best_dist serves as the value where the distances compete to see who is shortest
        for pkg in pending:
            d = lookup_distance(locate_address(truck.location),
                                locate_address(pkg.street))
            if d < best_dist:
                best_dist = d
                best = pkg

        # once best distance is found the following happens
        # 1. packages are appended to the trucks packages(emptied previously into the pending)
        # 2. newly delivered package is removed from pending
        # 3. necessary tracked data is updated
        truck.packages.append(best.ID)
        pending.remove(best)
        truck.miles += best_dist
        truck.location = best.street
        truck.time += datetime.timedelta(hours=best_dist / 18)
        best.delivery = truck.time
        best.departure = truck.departure

if __name__ == '__main__':
    run_route(truck1)
    run_route(truck3)
    # since there are only two drivers, one truck needs to wait for one to finish
    truck2.departure = min(truck1.time, truck3.time)
    run_route(truck2)

    print("The overall miles are:", truck1.miles + truck2.miles + truck3.miles)
    print("Truck 1:", truck1.miles)
    print("Truck 2:", truck2.miles)
    print("Truck 3:", truck3.miles)

    # simple user entry, can put in a package id and a time in the correct format
    while True:
        t = input("Enter Time Format: HH:MM. ")
        h, m = t.split(":")
        moment = datetime.timedelta(hours=int(h), minutes=int(m))
        try:
            ids = [int(input("Package id number/leave blank:"))]
        except ValueError:
            ids = range(1, 41)

        # data display
        for pid in ids:
            pkg = table.search(pid)
            pkg.update_status(moment)
            print(pkg)
