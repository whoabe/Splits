class Line(object):
    def __init__(self, TL_y, BR_y):
        # TL = Top Left
        # BR = Bottom Right
        self.TL_y = TL_y
        self.BR_y = BR_y


    # def area(self):
    #     return ((self.BR_x-self.TL_x)*(self.TL_y-self.BR_y)


    def inside_line(self, y_low, y_high):
        if self.TL_y >= y_low and self.BR_y <= y_high:
            return True
        else:
            return False