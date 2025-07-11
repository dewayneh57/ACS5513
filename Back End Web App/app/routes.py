from flask import Blueprint, request, jsonify
from app.services.pricing_engine import PricingEngine

api = Blueprint('api', __name__)
pricing_engine = PricingEngine()

@api.route('/api/train', methods=['POST'])
def train():
    data = request.get_json()
    features = data.get('features')
    prices = data.get('prices')
    
    if not features or not prices:
        return jsonify({'error': 'Features and prices are required'}), 400
    
    pricing_engine.train_model(features, prices)
    return jsonify({'message': 'Model trained successfully'}), 200

@api.route('/api/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        features = data.get('features')
        if not features:
            return jsonify({'error': 'Features are required for prediction'}), 400
    else:  # GET
        features = {
            'bedrooms': request.args.get('bedrooms', type=int),
            'bathrooms': request.args.get('bathrooms', type=float),
            'sqft': request.args.get('sqft', type=int),
            'year_built': request.args.get('year_built', type=int),
            'location': request.args.get('location', type=str)
        }
        features = {k: v for k, v in features.items() if v is not None}
        if not features:
            return jsonify({'error': 'Features are required for prediction'}), 400

    try:
        price = pricing_engine.predict_price(features)
        message = "Price generated successfully."
    except Exception as e:
        price = None
        message = f"Error generating price: {str(e)}"

    response = {
        **features,
        'price': price,
        'message': message if price is None else None
    }
    return jsonify(response), 200

def register_routes(app):
    app.register_blueprint(api)