class Area(object):
    def __init__(self, TL_x, TL_y, BR_x, BR_y):
        # TL = Top Left
        # BR = Bottom Right
        self.TL_x = TL_x
        self.TL_y = TL_y
        self.BR_x = BR_x
        self.BR_y = BR_y


    # def area(self):
    #     return ((self.BR_x-self.TL_x)*(self.TL_y-self.BR_y)


    def abcde(self, x, y):
        if x >= self.TL_x and x <= self.BR_x and y >= self.TL_y and y <= self.BR_y:
            return True
        else:
            return False