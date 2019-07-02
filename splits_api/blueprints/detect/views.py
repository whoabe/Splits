from flask import Blueprint, jsonify
from models.receipt_details import Receipt_details
from models.receipt import Receipt

detect_api_blueprint = Blueprint('detect_api',
                             __name__,
                             template_folder='templates')

@detect_api_blueprint.route('/<receipt_id>', methods=['GET'])
def index(receipt_id):
    receipt = Receipt.get_by_id(receipt_id)
    if receipt:
        receipt_details = Receipt_details.select().where(Receipt_details.receipt_id==receipt.id)

        dict_list = []
        for i in receipt_details:

            dict = {
                'coords':i.coords, 'text':i.text
            }
            dict_list.append(dict)

        return jsonify(dict_list)
    return "detect API, want a dictionary that contains the coord as key and text as value"
