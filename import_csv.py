import csv
from cride.circles.models import Circle


def import_csv_circles(csv_filename):
    with open(csv_filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            circle = Circle(**row)
            circle.save()
            print(row)
