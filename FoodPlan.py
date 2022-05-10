from TimeSlot import TimeSlot
from TimeSlot import TimeSlotType
from constraints import Constraint
from constraints import ConstraintType
from collections import defaultdict
import csv


class FoodPlan(object):
    WEEKS_IN_MONTH = 4
    DAYS_IN_WEEKS = 7

    def __init__(self, constraints: list[Constraint]):
        # construct the root node
        self.rootNode = TimeSlot(TimeSlotType.root, "root")
        # construct the month node
        monthNode = TimeSlot(TimeSlotType.month, "month", self.rootNode)

        # construct each week node
        dayCount = 0
        for i in range(self.WEEKS_IN_MONTH):
            weekNode = TimeSlot(TimeSlotType.week, "week" + str(i).zfill(2), monthNode)
            for j in range(self.DAYS_IN_WEEKS):
                dayNode = TimeSlot(TimeSlotType.day, "day" + str(dayCount).zfill(3), weekNode)
                morningNode = TimeSlot(TimeSlotType.morning, "morning" + str(dayCount).zfill(3), dayNode)
                afternoonNode = TimeSlot(TimeSlotType.afternoon, "afternoon" + str(dayCount).zfill(3), dayNode)
                dayCount += 1

        # adding constraints to it
        constraintMap = defaultdict(lambda: [])
        for constraint in constraints:
            constraintMap[constraint.timeSlot].append(constraint)
        allTimeSlots = self.getAllTimeSlot()
        for timeSlot in allTimeSlots:
            for constraint in constraintMap[timeSlot.type]:
                self.addConstraintToTimeSlot(timeSlot, constraint)

    def __repr__(self):
        allTimeSlots = self.getAllTimeSlot()
        result = ""
        # print the first 10 slot for debugging
        for i in range(len(allTimeSlots)):
            result += str(allTimeSlots[i]) + "\n"
        return result

    def getAllTimeSlot(self):
        allTimeSlots = []
        stack = [self.rootNode]
        while stack:
            node = stack.pop()
            allTimeSlots.append(node)
            stack.extend(node.children)
        return allTimeSlots

    @staticmethod
    def addConstraintToTimeSlot(node: TimeSlot, constraint: Constraint):
        if constraint.op == ConstraintType.need_class:
            node.addNeed(constraint.target, constraint.num)
        elif constraint.op == ConstraintType.cooldown_class:
            node.addCoolDownClass(constraint.target, constraint.num)
        elif constraint.op == ConstraintType.cooldown_item:
            node.addCoolDownItem(constraint.target, constraint.num)
        elif constraint.op == ConstraintType.max_item:
            node.addMaxItem(constraint.target, constraint.num)
        elif constraint.op == ConstraintType.max_dis_class:
            node.addMaxDisClass(constraint.target, constraint.num)
        elif constraint.op == ConstraintType.add_item:
            child = node.descendants[constraint.num]
            child.addFood(constraint.target)

    def outputToScreen(self):
        for timeSlot in self.rootNode.descendants:
            print("{}\t{}".format(timeSlot.name, str(timeSlot.food)))

    def outputToCsv(self, filePath):
        with open(filePath, 'w') as csvFile:
            csvWriter = csv.writer(csvFile)
            for timeSlot in self.rootNode.descendants:
                row = [timeSlot.name]
                row.extend(timeSlot.food)
                csvWriter.writerow(row)
