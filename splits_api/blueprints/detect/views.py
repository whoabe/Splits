from flask import Blueprint, jsonify, request
from models.receipt_details import Receipt_details
from models.receipt import Receipt
from area import Area

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


@detect_api_blueprint.route('/<receipt_id>', methods=['GET'])
def index2(receipt_id):
    # takes in the click coords and receipt id and returns the text value if it exists within one of the box coords

    # clicked_coords = request.form.get('coords')
    clicked_coords = [1500, 1600] #test case
    #should output RM15.09

    clicked_coords_x = clicked_coords[0]
    clicked_coords_y = clicked_coords[1]    

    receipt = Receipt.get_by_id(receipt_id)

    if receipt:
        receipt_details = Receipt_details.select().where(Receipt_details.receipt_id==receipt.id)

        for i in receipt_details:
            # check each item in receipt_details to see if the CC is in the box
            tuple_coords = eval(i.coords)
            TL_x = tuple_coords[0][0]
            TL_y = tuple_coords[0][1]
            BR_x = tuple_coords[1][0]
            BR_y = tuple_coords[1][1]
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

            if test2.abcde(clicked_coords_x, clicked_coords_y) == True:
                return jsonify(i.text)


    # takes clicked coords, runs it through the query with the receipt_id and returns the text value, else return none
    return 'not found'