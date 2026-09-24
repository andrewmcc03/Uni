from flask import Flask, jsonify, make_response

app = Flask(__name__)

businesses =  [
    {
        "id" : 1,
        "name" : "Pizza Mountain",
        "town" : "Coleraine",
        "rating" : 5,
        "reviews" : []  
    },
    {
        "id" : 2,
        "name" : "Wine Lake",
        "town" : "Ballymoney",
        "rating" : 3,
        "reviews" : []         
    },
    {
        "id" : 3,
        "name" : "Sweet Desert",
        "town" : "Ballymena",
        "rating" : 4,
        "reviews" : []
    }
]

@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    return make_response( jsonify( businesses ), 200 )

@app.route("/api/v1.0/businesses/<int:id>", methods=["GET"])
def show_one_business(id):
    data_to_return =  [ business for business in businesses if business["id"] == id ]
    return make_response( jsonify(  data_to_return[0] ), 200 )

if __name__ == "__main__":
    app.run(debug=True)
