from database.db import (
    add_new_couriers,
    update_courier_info,
    add_new_orders,
    flask_application,
    database,
    add_courier_orders,
    orders_complete,
    courier_info,
)
from flask import Response, request


with flask_application.app_context():
    database.create_all()


@flask_application.route("/couriers", methods=["POST"])
def post_couriers():
    try:
        couriers = request.json["data"]
        success, answer = add_new_couriers(couriers)
    except Exception:
        return Response({}, status=400, mimetype="application/json")
    else:
        if success:
            return Response(answer, status=201, mimetype="application/json")
        else:
            return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/couriers/<int:courier_id>", methods=["PATCH"])
def patch_courier(courier_id):
    try:
        parameter = request.json
        success, answer = update_courier_info(courier_id, parameter)
    except Exception:
        return Response({}, status=400, mimetype="application/json")
    else:
        if success:
            return Response(answer, status=200, mimetype="application/json")
        else:
            return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/orders", methods=["POST"])
def post_orders():
    try:
        orders = request.json["data"]
        success, answer = add_new_orders(orders)
    except Exception:
        return Response({}, status=400, mimetype="application/json")
    else:
        if success:
            return Response(answer, status=201, mimetype="application/json")
        else:
            return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/orders/assign", methods=["POST"])
def assign_orders():
    try:
        courier = request.json["courier_id"]
        success, answer = add_courier_orders(courier)
    except Exception:
        return Response({}, status=400, mimetype="application/json")
    else:
        if success:
            return Response(answer, status=201, mimetype="application/json")
        else:
            return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/orders/complete", methods=["POST"])
def complete_orders():
    try:
        data = request.json
        success, answer = orders_complete(data)
    except Exception:
        return Response({}, status=400, mimetype="application/json")
    else:
        if success:
            return Response(answer, status=200, mimetype="application/json")
        else:
            return Response(answer, status=400, mimetype="application/json")


@flask_application.route("/couriers/<int:courier_id>", methods=["GET"])
def get_courier_info(courier_id):
    return courier_info(courier_id)


if __name__ == "__main__":
    flask_application.run(host="0.0.0.0", port="8080")
