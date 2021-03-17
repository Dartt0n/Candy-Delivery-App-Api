from database.db_model import flask_application as app, database


with app.app_context():
    database.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
