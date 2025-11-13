# Avery Johnson WGU Delivery Application
# Student ID:011430854
import csv
import datetime

# remove these two to other file if needed or maybe do it in main we'll see
with open("csv/address.csv") as addressCSV:
    AddressCSV = csv.reader(addressCSV)
    AddressCSV = list(AddressCSV)
with open("csv/distance.csv") as distanceCSV:
    DistanceCSV = csv.reader(distanceCSV)
    DistanceCSV = list(DistanceCSV)


# below two classes to be moved out
# the next step is creating my own hash table
class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = []
        for i in range(capacity):
            self.table.append([])

    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                keyValue[1] = value
                return True
        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    # searches keyvalue for the correct key (keyValue[0])
    # and returns correct value keyValue[1]
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                return keyValue[1]
        return None

    # searches keyvalue for the correct key and deletes it
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)

class Package:
    def __init__(self, id, street, city, state, zip, deadline, weight, notes, status, departure, delivery):
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departure = departure
        self.delivery = delivery

    def __str__(self):
        return ("ID: %s, %-20s, %s, %s,%s, Deadline: %s,%s,%s,Departure Time: %s,Delivery Time: %s" %
                (self.id, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departure, self.delivery))

    def update_status(self, hasTimeChanged):
        if self.delivery == None:
            self.status = "HUB"
        elif hasTimeChanged < self.delivery:
            self.status = "Out for delivery"
        else:
            self.status = "Delivered"

def load_packages(filepath):
    with open(filepath) as packagesCSV:
        packageData = csv.reader(packagesCSV, delimiter=',')
        next(packageData)
        for package in packageData:
            id = int(package[0])
            street = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deadline = package[5]
            weight = package[6]
            notes = package[7]
            status = "HUB"
            departure = None
            delivery = None

            p = Package(id, street, city, state, zip, deadline, weight, notes, status, departure, delivery)

            packageTable.insert(id, p)

packageTable = HashTable(40)

class Truck:
    def __init__(self, speed, miles, location, departure, packages):
        self.speed = speed
        self.miles = miles
        self.location = location
        self.time = departure
        self.departure = departure
        self.packages = packages

def address_helper(address):
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])
    return None

def distance_calculator(address1, address2):
    distance = DistanceCSV[address1][address2]
    # flips the argument so that distances may be calculated in either order
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)

load_packages("csv/package.csv")

def deliver_packages(truck):
    deliveryRoute = []
    for id in truck.packages:
        package = packageTable.search(id)
        deliveryRoute.append(package)

    truck.packages.clear()
    while len(deliveryRoute) > 0:
        nextAddressDistance = 1000
        nextPackage = None
        for package in deliveryRoute:
            if distance_calculator(address_helper(truck.location), address_helper(package.street)) <= nextAddressDistance:
                nextAddressDistance = distance_calculator(address_helper(truck.location), address_helper(package.street))
                nextPackage = package
        truck.packages.append(nextPackage.id)
        deliveryRoute.remove(nextPackage)
        truck.miles += nextAddressDistance
        truck.currentLocation = nextPackage.street + nextPackage.city
        truck.time += datetime.timedelta(hours=nextAddressDistance / 18)
        nextPackage.delivery = truck.time
        nextPackage.departure = truck.departure


if __name__ == '__main__':
    truck1 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                    [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
    truck2 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),
                    [2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
    truck3 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                    [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])

    # Actually calls the trucks to leave to being delivering packages
    deliver_packages(truck1)
    deliver_packages(truck3)
    # ensures truck 2 won't leave until either truck 1 or 2 have returned
    truck2.departure = min(truck1.time, truck3.time)
    deliver_packages(truck2)

    print("The overall miles are:", (truck1.miles + truck2.miles + truck3.miles))

    while True:
        userTime = input("Enter Time Format: HH:MM. ")
        (h, m) = userTime.split(":")
        timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
        try:
            singleEntry = [int(input("Package id number/leave blank:"))]
        except ValueError:
            singleEntry = range(1, 41)
        for packageID in singleEntry:
            package = packageTable.search(packageID)
            package.update_status(timeChange)
            print(str(package))


# total distance for all trucks needs to be put below 140 trucks

