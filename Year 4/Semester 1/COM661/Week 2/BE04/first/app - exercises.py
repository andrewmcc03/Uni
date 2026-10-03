from flask import Flask, jsonify, make_response, request
import uuid, random

app = Flask(__name__)

businesses =  {}

def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast','Lisburn', 'Ballymena', 'Derry', 'Newry', 'Enniskillen', 'Omagh', 'Ballymoney']
    businesses_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[random.randint(0, len(towns) - 1)]
        rating = random.randint(1, 5)
        businesses_dict[id] = {
            "name" : name,
            "town" : town,
            "rating" : rating,
            "reviews" : {}
        }
    return businesses_dict

@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)
    businesses_list = [ { k : v } for k, v in businesses.items() ]
    
    return make_response( jsonify( businesses_list[page_start : page_start + page_size] ), 200 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    if id in businesses:
        return make_response( jsonify( businesses[id] ), 200 )
    else:
        return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )

@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        next_id = str(uuid.uuid1())
        new_business = {
            "name" : request.form["name"],
            "town" : request.form["town"],
            "rating" : request.form["rating"],
            "reviews" : {}
        }
        businesses[next_id] = new_business
        return make_response( jsonify( { next_id : new_business } ), 201 )
    else:
        return make_response( jsonify( { "error" : "Missing form data." } ), 400 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if id not in businesses:
        return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )
    else:
        if not "name" in request.form and not "town" in request.form and not "rating" in request.form:
            return make_response( jsonify( { "error" : "Missing form data." } ), 400 )
        else:
            if "name" in request.form:
                businesses[id]["name"] = request.form["name"]
            if "town" in request.form:
                businesses[id]["town"] = request.form["town"]
            if "rating" in request.form:
                businesses[id]["rating"] = request.form["rating"]
            return make_response( jsonify( { id : businesses[id] } ), 200 )            

@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    if id in businesses:
        del businesses[id]
        return make_response( jsonify( {} ), 200 )
    else:
        return make_response( jsonify( { "error" : "Invalid business ID." } ), 404 )

@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["GET"])
def fetch_all_reviews(b_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID."}), 404)

    page_num, page_size = 1, 5
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)
    reviews_list = [ { k : v } for k, v in businesses[b_id]["reviews"].items() ]
    
    return make_response(jsonify(reviews_list[page_start : page_start + page_size]), 200)

@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID."}), 404)
    if "username" not in request.form or "comment" not in request.form or "stars" not in request.form:
        return make_response(jsonify({"error": "Missing form data."}), 400)

    review_id = str(uuid.uuid1())
    businesses[b_id]["reviews"][review_id] = {
        "username": request.form["username"],
        "comment": request.form["comment"],
        "stars": request.form["stars"]
    }
    return make_response(jsonify({review_id: businesses[b_id]["reviews"][review_id]}), 201)

@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID."}), 404)
    if r_id not in businesses[b_id]["reviews"]:
        return make_response(jsonify({"error": "Invalid review ID."}), 404)
    return make_response(jsonify({r_id: businesses[b_id]["reviews"][r_id]}), 200)

@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID."}), 404)
    if r_id not in businesses[b_id]["reviews"]:
        return make_response(jsonify({"error": "Invalid review ID."}), 404)

    if not ("username" in request.form and "comment" in request.form and "stars" in request.form):
        return make_response( jsonify( { "error" : "Missing form data." } ), 400 )
    else:
        if "username" in request.form:
            businesses[b_id]["reviews"][r_id]["username"] = request.form["username"]
        if "comment" in request.form:
            businesses[b_id]["reviews"][r_id]["comment"] = request.form["comment"]
        if "stars" in request.form:
            businesses[b_id]["reviews"][r_id]["stars"] = request.form["stars"]
        return make_response(jsonify({r_id: businesses[b_id]["reviews"][r_id]}), 200)

@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID."}), 404)
    if r_id not in businesses[b_id]["reviews"]:
        return make_response(jsonify({"error": "Invalid review ID."}), 404)

    del businesses[b_id]["reviews"][r_id]
    return make_response(jsonify({}), 200)

if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug=True, port=4999)
