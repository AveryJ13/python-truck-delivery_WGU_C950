import datetime


class Package:
    def __init__(self, ID, street, city, state, zip, deadline, weight, notes, status, departure, delivery):
        self.ID = ID
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
                (self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departure, self.delivery))

    def update_status(self, timeChange):
        if self.delivery == None:
            self.status = "HUB"
        elif timeChange < self.departure:
            self.status = "HUB"
        elif timeChange < self.delivery:
            self.status = "Out for delivery"
        else:
            self.status = "Delivered"
        if self.ID == 9:  # will change the address for package 9 after the alloted time
            if timeChange > datetime.timedelta(hours=10, minutes=20):
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"