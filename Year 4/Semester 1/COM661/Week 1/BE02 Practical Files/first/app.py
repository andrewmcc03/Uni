from flask import Flask, make_response, jsonify

app = Flask(__name__)

businesses = [
    {
        "id": 1,
        "name": "Holy Smokes",
        "town": "Coleraine",
        "rating": 5,
        "reviews": []
    },
    {
        "id": 2,
        "name": "Tesco",
        "town": "Newtownabbey",
        "rating": 3,
        "reviews": []
    },
    {
        "id": 3,
        "name": "ASDA",
        "town": "Ballyclare",
        "rating": 4,
        "reviews": []
    }
]

@app.route("/api/1.0/businesses", methods=["GET"])
def show_all_businesses():
    return make_response( jsonify( businesses ), 200)

@app.route("/api/1.0/businesses/<int:id>", methods=["GET"])
def show_one_business(id):
    data_to_return = [business for business in businesses if business["id"] == id]
    return make_response( jsonify( data_to_return[0] ), 200)

# @app.route('/', methods=['GET'])
# def index():
#     return make_response("<h1>Hello, World!</h1>", 200)

# @app.route('/com661', methods=['GET'])
# def com661():
#     return make_response("<h1>Welcome to COM661!</h1>", 200)

# @app.route('/module/<string:code>', methods=['GET'])
# def module(code):
#     return make_response(f"<h1>Welcome to the {code} module!</h1>", 200)

if __name__ == '__main__':
    app.run(debug=True)