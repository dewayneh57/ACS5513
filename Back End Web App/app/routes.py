from flask import Blueprint, request, jsonify

from flask import current_app
api = Blueprint('api', __name__)

@api.route('/api/train', methods=['POST'])
def train():
    data = request.get_json()
    features = data.get('features')
    prices = data.get('prices')
    
    if not features or not prices:
        return jsonify({'error': 'Features and prices are required'}), 400
    
    current_app.pricing_engine.train_model(features, prices)
    return jsonify({'message': 'Model trained successfully'}), 200

@api.route('/api/predict_with_model', methods=['POST'])
def predict_with_model():
    data = request.get_json()
    
    if not data:
        print(f"Request data is required")
        return jsonify({'error': 'Request data is required'}), 400
    
    model_name = data.get('model_type', 'catboost')
    features = data.get('features', {})

    # Allow empty or missing features - they will be set to 0 in the pricing engine
    if features is None:
        features = {}
        print("Warning: No features provided, will use default values (0)")
    
    try:
        prediction = current_app.pricing_engine.predict_with_model(model_name, features)
        
        response = {
            'model_used': model_name,
            'predicted_price': prediction,
            'features': features,
            'success': True
        }
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Prediction failed for model {model_name}: {str(e)}")
        response = {
            'error': f"Prediction failed: {str(e)}",
            'model_used': model_name,
            'success': False
        }
        return jsonify(response), 500

@api.route('/api/models', methods=['GET'])
def get_available_models():
    """Get list of available models"""
    available_models = []
    for model_name, model in current_app.pricing_engine.models.items():
        available_models.append({
            'name': model_name,
            'available': model is not None
        })
    
    return jsonify({'models': available_models}), 200

def register_routes(app):
    app.register_blueprint(api)