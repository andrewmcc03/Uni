from flask import Flask, jsonify, make_response, request

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

@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    next_id = businesses[-1]["id"] + 1
    new_business = {
        "id" : next_id,
        "name" : request.form["name"],
        "town" : request.form["town"],
        "rating" : request.form["rating"],
        "reviews" : []
    }
    businesses.append(new_business)
    return make_response( jsonify( new_business ), 201 )

@app.route("/api/v1.0/businesses/<int:id>", methods=["PUT"])
def edit_business(id):
    for business in businesses:
        if business["id"] == id:
            business["name"] = request.form["name"]
            business["town"] = request.form["town"]
            business["rating"] = request.form["rating"]
            break
    return make_response( jsonify( business ), 200 )

@app.route("/api/v1.0/businesses/<int:id>", methods=["DELETE"])
def delete_business(id):
    for business in businesses:
        if business["id"] == id:
            businesses.remove(business)
            break
    return make_response( jsonify( {} ), 200 )

@app.route("/api/v1.0/businesses/<int:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    for business in businesses:
        if business["id"] == id:
            break
    return make_response( jsonify( business["reviews"] ), 200 )

@app.route("/api/v1.0/businesses/<int:id>/reviews", methods=["POST"])
def add_new_review(id):
    for business in businesses:
        if business["id"] == id:
            if len(business["reviews"]) == 0:
                new_review_id = 1
            else:
                new_review_id = business["reviews"][-1]["id"] + 1
        new_review = {
            "id" : new_review_id,
            "username" : request.form["username"],
            "comment" : request.form["comment"],
            "stars" : request.form["stars"]
        }
        business["reviews"].append(new_review)
        break
    return make_response( jsonify( new_review ), 201 )

@app.route("/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    break
            break
    return make_response( jsonify( review ), 200 )

@app.route("/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    review["username"] = request.form["username"]
                    review["comment"] = request.form["comment"]
                    review["stars"] = request.form["stars"]
                    break
            break
    return make_response( jsonify( review ), 200 )

@app.route("/api/v1.0/businesses/<int:b_id>/reviews/<int:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    business["reviews"].remove(review)
                    break
            break
    return make_response( jsonify( {} ), 200 )

if __name__ == "__main__":
    app.run(debug=True, port=4999)
