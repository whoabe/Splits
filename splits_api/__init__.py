from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from splits_api.blueprints.users.views import users_api_blueprint

from splits_api.blueprints.detect.views import detect_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

app.register_blueprint(detect_api_blueprint, url_prefix='/api/v1/detect')
