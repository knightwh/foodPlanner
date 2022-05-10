from input_reader import InputReader
from FoodPlan import FoodPlan
from FoodPlanner import FoodPlanner
import random

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    random.seed()

    foodMap, classMap = InputReader.read_food_list("../input/foodList.csv")
    print(foodMap)
    print(classMap)
    constraints = InputReader.read_constraint("../input/constraints.csv")
    print(constraints)
    foodPlan = FoodPlan(constraints)
    print(foodPlan)
    foodPlanner = FoodPlanner(foodPlan, classMap, foodMap)
    #print(foodPlanner.getNeedsMap())
    foodPlanner.plan()
    foodPlan.outputToScreen()
    foodPlan.outputToCsv("../output/first_month.csv")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
