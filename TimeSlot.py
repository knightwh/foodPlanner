import enum
from collections import defaultdict


class TimeSlotType(enum.Enum):
    root = 1
    month = 2
    week = 3
    day = 4
    morning = 5
    afternoon = 6


class TimeSlot(object):
    MAX_COOL_DOWN = 10000

    def __init__(self, timeSlotType: TimeSlotType, name: str, parent=None):
        self.type = timeSlotType
        self.name = name
        self.parent = parent
        self.children = []
        self.descendants = []
        self.food = set()
        self.descendantFood = defaultdict(lambda: 0)
        self.need = {}
        self.coolDownClass = {}
        self.coolDownItem = {}
        self.maxItem = {}
        self.maxDisClass = {}
        if parent:
            parent.addChildren(self)

    def __repr__(self):
        parent = self.parent.name if self.parent else "none"
        children = list(map(lambda c: c.name, self.children))
        descendants = list(map(lambda d: d.name, self.descendants))
        return "name:" + self.name + " | "\
            + "type:" + self.type.name + " | " \
            + "parent:" + parent + " | " \
            + "children:" + str(children) + " | " \
            + "descendants:" + str(descendants) + " | " \
            + "food:" + str(self.food) + " | " \
            + "need:" + str(self.need) + " | " \
            + "coolDownClass:" + str(self.coolDownClass) + " | " \
            + "coolDownItem:" + str(self.coolDownItem) + " | " \
            + "maxItem:" + str(self.maxItem) + " | " \
            + "maxDisClass:" + str(self.maxDisClass)

    def addNeed(self, foodClass, number):
        self.need[foodClass] = number

    def addCoolDownClass(self, foodClass, number):
        self.coolDownClass[foodClass] = number

    def addCoolDownItem(self, food, number):
        self.coolDownItem[food] = number

    def addChildren(self, child):
        self.children.append(child)
        self.refresh()

        if self.parent:
            self.parent.refresh()

    def refresh(self):
        # Recalculate the descendant list
        self.descendants = []
        for child in self.children:
            if not child.isEndSlot():
                self.descendants.extend(child.descendants)
            else:
                self.descendants.append(child)

        # Recalculate the descendant food list
        self.descendantFood = defaultdict(lambda: 0)
        for descendant in self.descendants:
            for food in descendant.food:
                self.descendantFood[food] += 1

        if self.parent:
            self.parent.refresh()

    def addFoodTree(self, food):
        self.descendantFood[food] += 1
        if self.parent:
            self.parent.addFoodTree(food)

    def removeFoodTree(self, food):
        self.descendantFood[food] -= 1
        if self.parent:
            self.parent.removeFoodTree(food)

    def addFood(self, food):
        self.food.add(food)
        self.addFoodTree(food)

    def removeFood(self, food):
        self.food.remove(food)
        self.removeFoodTree(food)

    def addMaxItem(self, food, number):
        self.maxItem[food] = number

    def addMaxDisClass(self, fClass, number):
        self.maxDisClass[fClass] = number

    def checkCanAddFood(self, food, foodMap):
        # self policy check, to see whether duplicated
        if food in self.food:
            return False
        # parent policy check
        if self.parent:
            return self.parent.checkCanAddFoodAtChild(food, foodMap, self)
        return True

    def checkCanAddFoodAtChild(self, food, foodMap, child):
        # check for max item policy
        if food in self.maxItem and self.descendantFood[food] >= self.maxItem[food]:
            return False

        # Check for max distinguish food policy
        fClass = foodMap[food]
        if fClass in self.maxDisClass and food not in self.descendantFood:
            count = 0
            for item in self.descendantFood:
                if foodMap[item] == fClass:
                    count += 1
            if count >= self.maxDisClass[fClass]:
                return False

        # Check for cooldown policy
        cooldown = self.MAX_COOL_DOWN
        if food in self.coolDownItem:
            cooldown = self.coolDownItem[food]
        if foodMap[food] in self.coolDownClass:
            cooldown = min(cooldown, self.coolDownClass[foodMap[food]])
        #print("{}:{}:cooldown={}".format(self.type, food, str(cooldown)))
        if cooldown < self.MAX_COOL_DOWN:
            # locate the child
            childIdx = -1
            for i in range(len(self.descendants)):
                if self.descendants[i] == child:
                    childIdx = i
                    break
            for i in range(max(0, childIdx - cooldown), min(len(self.descendants), childIdx + cooldown + 1)):
                if food in self.descendants[i].food:
                    return False

        if self.parent:
            return self.parent.checkCanAddFoodAtChild(food, foodMap, child)

        return True

    def isEndSlot(self):
        return self.type == TimeSlotType.morning or self.type == TimeSlotType.afternoon
