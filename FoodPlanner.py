from FoodPlan import FoodPlan
from collections import defaultdict
import random


class FoodPlanner(object):
    MAXIMUM_TRAIL = 1

    def __init__(self, foodPlan: FoodPlan, classMap, foodMap):
        self.foodPlan = foodPlan
        self.classMap = classMap
        self.foodMap = foodMap

    def getNeedsMap(self):
        needsMap = defaultdict(lambda: [])
        allTimeSlots = self.foodPlan.getAllTimeSlot()
        for timeSlot in allTimeSlots:
            if timeSlot.isEndSlot():
                hasPlanned = defaultdict(lambda: 0)
                for food in timeSlot.food:
                    hasPlanned[self.foodMap[food]] += 1
                for fClass, count in timeSlot.need.items():
                    if count > hasPlanned[fClass]:
                        needsMap[fClass].append((timeSlot, count - hasPlanned[fClass]))
        for key, value in needsMap.items():
            value.sort(key=lambda x: str(10 - x[1]) + x[0].name)
            newValue = []
            for timeSlot, count in value:
                for i in range(count):
                    newValue.append(timeSlot)
            needsMap[key] = newValue
        return needsMap

    def plan(self):
        needsMap = self.getNeedsMap()
        for fClass in needsMap:
            if not self.planForClass(fClass, needsMap[fClass]):
                print("Failed to generated plan for category:" + fClass)
                return None
        print("planing done")
        return self.foodPlan

    def planForClass(self, fClass: str, timeSlotList):
        triedFood = [set() for i in range(len(timeSlotList))]
        lastAddFood = ["" for i in range(len(timeSlotList))]
        allFood = self.classMap[fClass]
        idx = 0
        attamp = 0
        while idx < len(timeSlotList):
            candidates = list(allFood - triedFood[idx])
            if not candidates:
                if idx == 0:
                    return False
                # back trace
                triedFood[idx] = set()
                idx -= 1
                triedFood[idx].add(lastAddFood[idx])
                timeSlotList[idx].removeFood(lastAddFood[idx])
                attamp += 1
                if attamp % 1000 == 0:
                    print("Attamped {} times at idx {}".format(attamp, idx))
            else:
                food = candidates[random.randrange(len(candidates))]
                if timeSlotList[idx].checkCanAddFood(food, self.foodMap):
                    timeSlotList[idx].addFood(food)
                    lastAddFood[idx] = food
                    idx += 1
                else:
                    triedFood[idx].add(food)
        return True
