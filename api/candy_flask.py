from flask import Flask, request, Response
from database.db_worker import (
    add_new_couriers,
    update_courier_info,
    add_new_orders,
    add_courier_orders,
    orders_complete,
    courier_info,
)


flask_application = Flask(__name__)


@flask_application.route("/couriers", methods=["POST"])
def post_couriers():
    couriers = request.json["data"]
    success, answer = add_new_couriers(couriers)
    if success:
        return Response(answer, status=201, mimetype="application/json")
    else:
        return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/couriers/<int:courier_id>", methods=["PATCH"])
def patch_courier(courier_id):
    parameter = request.json
    success, answer = update_courier_info(courier_id, parameter)
    if success:
        return Response(answer, status=200, mimetype="application/json")
    else:
        return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/orders", methods=["POST"])
def post_orders():
    orders = request.json["data"]
    success, answer = add_new_orders(orders)
    if success:
        return Response(answer, status=201, mimetype="application/json")
    else:
        return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/orders/assign", methods=["POST"])
def assign_orders():
    courier = request.json["courier_id"]
    success, answer = add_courier_orders(courier)
    if success:
        return Response(answer, status=201, mimetype="application/json")
    else:
        return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/orders/complete", methods=["POST"])
def complete_orders():
    data = request.json
    success, answer = orders_complete(data)
    if success:
        return Response(answer, status=200, mimetype="application/json")
    else:
        return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/couriers/<int:courier_id>", methods=["GET"])
def get_courier_info(courier_id):
    return courier_info(courier_id)
