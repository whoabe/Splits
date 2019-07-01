from models.receipt import Receipt
import peewee as pw
from playhouse.hybrid import hybrid_property

class Receipt_details(Receipt):
    text = pw.CharField(unique=False, null = True)
    coords = pw.CharField(unique=False, null = True)

''' 
defining these functions to make it easier to output the values
'''
    # @hybrid_property
    # def coords(self):
    #     if self.receipt_coords:
    #         return self.receipt_coords

    # @hybrid_property
    # def text(self):
    #     if self.receipt_text:
    #         return self.receipt_text