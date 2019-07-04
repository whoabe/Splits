from flask import Blueprint, jsonify, request
from models.receipt_details import Receipt_details
from models.receipt import Receipt
from area import Area
from line import Line
from helpers import RepresentsInt
import re

detect_api_blueprint = Blueprint('detect_api',
                             __name__,
                             template_folder='templates')

# @detect_api_blueprint.route('/<receipt_id>', methods=['GET'])
# def index(receipt_id):
#     '''
#     provides data of dictionaries in a list
#     '''
#     receipt = Receipt.get_by_id(receipt_id)
#     if receipt:
#         receipt_details = Receipt_details.select().where(Receipt_details.receipt_id==receipt.id)

#         dict_list = []
#         for i in receipt_details:

#             dict = {
#                 'coords':i.coords, 'text':i.text
#             }
#             dict_list.append(dict)

#         return jsonify(dict_list)
#     return "detect API, want a dictionary that contains the coord as key and text as value"

#-------------------------------------------------#
# below is a working api function
#-------------------------------------------------#
# @detect_api_blueprint.route('/<receipt_id>', methods=['POST'])
# def index2(receipt_id):
#     # takes in the click coords and receipt id and returns the text value if it exists within one of the box coords

#     # clicked_coords = request.form.get('coords')
#     # clicked_coords = [1500, 1600] #test case
#     # #should output RM15.09

#     clicked_coords = request.get_data()
#     clicked_coords = clicked_coords.decode('utf-8')
#     clicked_coords = clicked_coords.split(',')
    
#     clicked_coords_x = int(clicked_coords[0])
#     clicked_coords_y = int(clicked_coords[1])

#     receipt = Receipt.get_by_id(receipt_id)

#     if receipt:
#         receipt_details = Receipt_details.select().where(Receipt_details.receipt_id==receipt.id)
#         for i in receipt_details:
#             # check each item in receipt_details to see if the CC is in the box
#             tuple_coords = eval(i.coords)
#             TL_x = tuple_coords[0][0]
#             TL_y = tuple_coords[0][1]
#             BR_x = tuple_coords[1][0]
#             BR_y = tuple_coords[1][1]
#             '''
# test code, should return True, and i.text = RM15.09

# when receipt_id = 17

# clicked_coords = [1500, 1600] 
# clicked_coords_x = clicked_coords[0]
# clicked_coords_y = clicked_coords[1] 
# TL_x = 1448
# TL_y = 1578
# BR_x = 1699
# BR_y = 1637
#             '''

#             test2 = Area(TL_x, TL_y, BR_x, BR_y)

#             if test2.abcde(clicked_coords_x, clicked_coords_y) == True:
#                 return jsonify(i.text)


#     # takes clicked coords, runs it through the query with the receipt_id and returns the text value, else return none
#     return 'not found'

#-------------------------------------------------#
# next iteration
#-------------------------------------------------#
@detect_api_blueprint.route('/<receipt_id>', methods=['POST'])
def index2(receipt_id):
    # takes in the click coords and receipt id and returns the text value if it exists within one of the box coords

    # clicked_coords = request.form.get('coords')
    # clicked_coords = [1500, 1600] #test case
    # #should output RM15.09

    #obtains click coordinates from the user
    clicked_coords = request.get_data()
    clicked_coords = clicked_coords.decode('utf-8')
    clicked_coords = clicked_coords.split(',')
    
    clicked_coords_x = int(clicked_coords[0])
    clicked_coords_y = int(clicked_coords[1])

    receipt = Receipt.get_by_id(receipt_id)

    if receipt:
        receipt_details = Receipt_details.select().where(Receipt_details.receipt==receipt)
        for i in receipt_details:
            # check each item in receipt_details to see if the CC is in the box
            tuple_coords = eval(i.coords)
            TL_x = tuple_coords[0][0]
            TL_y = tuple_coords[0][1]
            BR_x = tuple_coords[1][0]
            BR_y = tuple_coords[1][1]

            if BR_x - TL_x < 20:
                TL_x -= 25
                BR_x += 25
            '''
test code, should return True, and i.text = RM15.09

when receipt_id = 17

clicked_coords = [1500, 1600] 
clicked_coords_x = clicked_coords[0]
clicked_coords_y = clicked_coords[1] 
TL_x = 1448
TL_y = 1578
BR_x = 1699
BR_y = 1637
            '''

            test2 = Area(TL_x, TL_y, BR_x, BR_y)

            if test2.inside(clicked_coords_x, clicked_coords_y) == True:
                # if the clicked coords are inside of a bound box of a certain item, then return the items that exist on the same row, in a list
                line_list = []
                height = BR_y - TL_y
                var_factor = 0.30
                y_low = TL_y - height * var_factor
                y_high = height * var_factor + BR_y
                for i in receipt_details:
                    # searching through receipt details to see what items exist in the range of these y coords y_low to y_high
                    tuple_coords = eval(i.coords)
                    TL_y = tuple_coords[0][1]
                    BR_y = tuple_coords[1][1]
                    line_instance = Line(TL_y, BR_y)
                    if line_instance.inside_line(y_low, y_high) == True:
                        line_list.append(i)
                largest_BR_x = 0        
                for i in line_list:
                    tuple_coords = eval(i.coords)
                    BR_x = tuple_coords[1][0]
                    if BR_x > largest_BR_x:
                        largest_BR_x = BR_x
                        subtotal = i.text
                        i_subtotal = i
                    #   want the largest_BR_x to be set as subtotal in the JSON
                    if RepresentsInt(i.text):
                        quantity = i.text
                        i_quantity = i
                    #remove the subtotal and qty from the list, join the remaining stuff and call it description
                subtotal_value = float((re.findall(r"(\d+[\,\.]\d{0,2})", subtotal))[0])
                # regex to extract price as a float out ex. RM15.09 -> 15.09

                quantity_value = float(quantity)

                line_list.remove(i_subtotal)
                line_list.remove(i_quantity)
                description_list = []
                for item in line_list:
                    description_list.append(item.text)
                description = ' '.join(description_list)
                
                unit_price = subtotal_value/quantity_value
                # find out the unit price by diving subtotal by quantity


                    # if BR_x is the biggest, then it is the subtotal
                    # if i.text == an integer, then it is the quantity
                    # the remaining elements are the description. the unit price might be thrown into the description
                    # calculate the unit price by dividing the subtotal by the qty

                return jsonify(description=description, quantity=quantity_value, unit_price = unit_price, subtotal=subtotal_value)
                # returns json with a list of all the items that exist in the row
                # want to output QTY, description, subtotal


    # takes clicked coords, runs it through the query with the receipt_id and returns the text value, else return none
    return 'not found'