import enum
from TimeSlot import TimeSlotType


class ConstraintType(enum.Enum):
    need_class = 1
    cooldown_class = 2
    cooldown_item = 3
    max_item = 4
    min_item = 5
    add_item = 6
    max_dis_class = 7


class Constraint(object):

    def __init__(self, timeSlot: TimeSlotType, constraintType: ConstraintType, target: str, num: int):
        self.timeSlot = timeSlot
        self.op = constraintType
        self.target = target
        self.num = num

    def __repr__(self):
        return self.timeSlot.name + "/" + self.op.name + "/" + self.target + ":" + str(self.num)
