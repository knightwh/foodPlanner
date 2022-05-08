from collections import defaultdict
import csv
from TimeSlot import TimeSlotType
from constraints import ConstraintType
from constraints import Constraint


class InputReader:

    @classmethod
    def read_food_list(cls, path):
        foodMap = {}
        classMap = defaultdict(lambda: set())

        with open(path, 'r', encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                food, fClass = row[0], row[1]
                foodMap[food] = fClass
                classMap[fClass].add(food)

        return foodMap, classMap

    @classmethod
    def read_constraint(cls, path):
        constraints = []

        with open(path, 'r', encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                timeSlot, constraintType, target, num =\
                    TimeSlotType[row[0]], ConstraintType[row[1]], row[2], int(row[3])
                constraints.append(Constraint(timeSlot, constraintType, target, num))

        return constraints
