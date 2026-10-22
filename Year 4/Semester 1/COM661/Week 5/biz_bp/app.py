from flask import Flask

from blueprints.businesses.businesses import businesses_bp
from blueprints.reviews.reviews import reviews_bp
from blueprints.auth.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(businesses_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)


###############################################################################################
# API documentation:    https://mccormick-a26-5657291.postman.co/documentation/58637944-9f212d95-72a5-46d9-8a73-5703eb3533fe/publish?workspaceId=b3dd8668-bdc4-4e1c-8800-b2d1e7d7effa&authFlowId=18c041b8-75fa-490a-87e4-9d001d356c16&_pmt=pmMTc5MDc4MDAxNjU5MA%253D%253D%257CPM.MjAyNi0wOS0zMFQxNDo1MjowOC4wMTFa
#                       https://documenter.getpostman.com/view/58637944/2sBYHUSfLu
###############################################################################################


if __name__ == "__main__":
    app.run(debug = True, port=4999)