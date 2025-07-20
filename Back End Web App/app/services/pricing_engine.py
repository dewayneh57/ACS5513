from ast import If
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os

#
# This is a mock model that gets used if none of the pre-trained models can be loaded.
# It generates a realistic mock prediction based on input features.
# This is useful for testing the application when the pre-trained models are not available.
#
class MockModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.is_mock = True
    
    #
    # This method generates a mock prediction based on input features.
    # It uses basic heuristics based on common house price factors to create a realistic prediction.
    # The prediction is returned as a list to match the expected output format.
    #    
    def predict(self, X):
        import random
        
        # Extract some basic features to make prediction somewhat realistic
        if isinstance(X, list) and len(X) > 0:
            if isinstance(X[0], list):
                features = X[0]  # First row of features
            else:
                features = X
        else:
            features = []
        
        # Use basic heuristics based on common house price factors
        base_price = 200000  # Base price
        
        if len(features) >= 4:  # If we have square footage data
            try:
                # Assuming features include square footages (positions 3-6)
                total_sf = sum([float(f) for f in features[3:7] if str(f).replace('.', '').replace('-', '').isdigit()])
                if total_sf > 0:
                    base_price = total_sf * random.uniform(80, 150)  # $80-150 per sq ft
            except:
                pass
        
        # Add some model-specific variation
        model_multipliers = {
            'catboost': random.uniform(0.95, 1.05),
            'xgboost': random.uniform(0.93, 1.07),
            'lightgbm': random.uniform(0.94, 1.06)
        }
        
        multiplier = model_multipliers.get(self.model_name, 1.0)
        predicted_price = base_price * multiplier
        
        # Return as numpy array to match sklearn interface
        return [predicted_price]

#
# This method initializes the PricingEngine, loading pre-trained models and preparing the environment.
# It sets up the models dictionary and attempts to load the dataset.
# If the dataset is not found, it will create mock models for testing purposes.
#
class PricingEngine:
    # This method initializes the PricingEngine, loading pre-trained models and preparing the environment.
    # It sets up the models dictionary and attempts to load the dataset.
    # If the dataset is not found, it will create mock models for testing purposes.
    def __init__(self):
        self.data = None
        self.model = None
        self.models = {}
        self.load_pre_trained_models()

    # This method initializes the PricingEngine, loading pre-trained models and preparing the environment.
    # It sets up the models dictionary and attempts to load the dataset.
    # If the dataset is not found, it will create mock models for testing purposes.    
    def load_pre_trained_models(self):
        # Load pre-trained models from PKL files with enhanced compatibility
        # Get the models directory - it's at the root of Back End Web App
        # __file__ is in app/services/, so go up 1 levels to get to Back End Web App root
        models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        
        # the model files and their expected names
        model_files = {
            'catboost': 'CatBoost.pkl',
            'xgboost': 'XGBoost.pkl',
            'lightgbm': 'LightGBM.pkl'
        }
        
        print(f"Looking for models in: {models_dir}")
        
        for model_name, filename in model_files.items():
            file_path = os.path.join(models_dir, filename)
            try:
                if os.path.exists(file_path):
                    # Try multiple loading strategies for Python version compatibility
                    model = self._load_pickle_with_compatibility(file_path)
                    if model is not None:
                        self.models[model_name] = model
                        print(f"Successfully loaded {model_name} model from {filename}")
                    else:
                        print(f"All loading methods failed for {model_name}")
                        # Create a mock model for testing
                        self.models[model_name] = MockModel(model_name)
                        print(f"Created mock {model_name} model for testing")
                else:
                    print(f"Warning: Could not find {filename} in {models_dir}")
                    self.models[model_name] = MockModel(model_name)
                    print(f"Created mock {model_name} model (file not found)")
            except Exception as e:
                print(f"Error loading {model_name} model: {str(e)}")
                self.models[model_name] = MockModel(model_name)
                print(f"Created mock {model_name} model due to error")
        
        print(f"Available models: {list(self.models.keys())}")

    # The PKL (Pickle) files were created with an earlier version of python and there are compatability 
    # issues when trying to load them with the current version.  This code attempts to load models using
    # multiple methods to ensure compatibility across different Python versions in case we change 
    # the Python version in the future.
    def _load_pickle_with_compatibility(self, filepath):
        
        # Method 1: Standard pickle load
        try:
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
                print(f"Loaded with standard pickle")
                return model
        except Exception as e:
            print(f"Standard pickle load failed: {e}")
        
        # Method 2: Try with different encoding (helps with Python 2/3 compatibility)
        try:
            with open(filepath, 'rb') as f:
                model = pickle.load(f, encoding='latin1')
                print(f"Loaded with latin1 encoding")
                return model
        except Exception as e:
            print(f"Latin1 encoding failed: {e}")
        
        # Method 3: Try with bytes encoding
        try:
            with open(filepath, 'rb') as f:
                model = pickle.load(f, encoding='bytes')
                print(f"Loaded with bytes encoding")
                return model
        except Exception as e:
            print(f"Bytes encoding failed: {e}")
        
        # Method 4: Try loading as joblib (common for sklearn models)
        try:
            import joblib
            model = joblib.load(filepath)
            print(f"Loaded with joblib")
            return model
        except Exception as e:
            print(f"Joblib load failed: {e}")
        
        # Method 5: Try with dill (more robust pickle alternative)
        try:
            import dill
            with open(filepath, 'rb') as f:
                model = dill.load(f)
                print(f"Loaded with dill")
                return model
        except Exception as e:
            print(f"Dill load failed: {e}")
        
        return None

    # Predict house price using the loaded model
    # This method takes a dictionary of features, prepares them for prediction, and returns the predicted price.
    # If the model is not loaded, it raises a ValueError.
    # Missing feature data is automatically set to 0 for graceful handling.
    def predict_with_model(self, model_name, features):
        if model_name not in self.models or self.models[model_name] is None:
            return f"Model {model_name} not available"
        
        try:
            # Handle case where features might be None or empty
            if not features:
                features = {}
                print(f"Warning: No features provided, using default values (0) for prediction")
            
            # Prepare feature data for prediction
            print(f"Preparing features for {model_name} model with data: {features}")
            features_df = self.prepare_features(features)
            print(f"Prepared features for {model_name} model: {features_df}")
            
            # Make prediction
            model = self.models[model_name]
            
            # Check if it's a mock model and add disclaimer
            if hasattr(model, 'is_mock') and model.is_mock:
                # For mock models, pass the original features as a list
                features_list = [
                    float(features.get('overall_qual', 0)),
                    float(features.get('year_built', 0)),
                    float(features.get('first_flr_sf', 0)),
                    float(features.get('second_flr_sf', 0)),
                    float(features.get('bsmt_living_sf', 0)),
                    float(features.get('garage_size', 0))
                ]
                prediction = model.predict([features_list])[0]
                return f"${prediction:,.2f} (Mock prediction - PKL files incompatible)"
            else:
                # For real models, use the engineered features DataFrame
                prediction = model.predict(features_df)[0]
                print(f"Prediction made with {model_name} model - result is ${prediction:,.2f}")
                return f"${prediction:,.2f}"
            
        except Exception as e:
            print(f"Prediction error for model {model_name}: {str(e)}")
            return f"Prediction error: {str(e)}"

    # Prepare features for model prediction
    # This method takes a dictionary of form data, calculates engineered features, and returns them as a DataFrame.
    # It matches the exact feature set that the trained models expect.
    # Missing feature data is set to 0 to handle incomplete requests from the frontend.
    def prepare_features(self, form_data):
        # Map frontend field names to model-expected field names
        field_mapping = {
            'kitchen_qual': 'kitchen_qual_ord',
            'exterior_qual': 'exter_qual_ord', 
            'heating_qual': 'heating_qc_ord',
            'basement_qual': 'bsmt_qual_ord',
            'fireplace_qual': 'fireplace_qu_ord',
            'garage_finish': 'garage_finish_ord'
        }
        
        # Create a mapped version of form_data
        mapped_data = {}
        for key, value in form_data.items():
            mapped_key = field_mapping.get(key, key)  # Use mapping if exists, otherwise use original key
            mapped_data[mapped_key] = value
        
        # Helper function to safely convert to float, handling empty strings and None values
        def safe_float(value, default=0):
            if value is None or value == '' or value == 'None':
                return float(default)
            try:
                return float(value)
            except (ValueError, TypeError):
                return float(default)
        
        # Extract basic values from mapped form data - set missing values to 0
        overall_qual = safe_float(mapped_data.get('overall_qual'), 0)  # Set to 0 if missing
        year_built = safe_float(mapped_data.get('year_built'), 0)
        year_remod_add = safe_float(mapped_data.get('year_remod_add'), year_built if year_built > 0 else 0)
        first_flr_sf = safe_float(mapped_data.get('first_flr_sf'), 0)
        second_flr_sf = safe_float(mapped_data.get('second_flr_sf'), 0)
        total_bsmt_sf = safe_float(mapped_data.get('bsmt_living_sf'), 0)
        garage_cars = safe_float(mapped_data.get('garage_cars'), 0)
        garage_area = safe_float(mapped_data.get('garage_size'), 0)  # Set to 0 if missing
        garage_yr_blt = safe_float(mapped_data.get('garage_yr_blt'), year_built if year_built > 0 else 0)
        garage_finish = safe_float(mapped_data.get('garage_finish_ord'), 0)  # 0=No garage/Unfinished
        full_bath = safe_float(mapped_data.get('full_baths'), 0)
        half_bath = safe_float(mapped_data.get('half_baths'), 0)
        ms_subclass = safe_float(mapped_data.get('ms_subclass'), 0)  # Set to 0 if missing
        
        # Quality ordinal mappings - set to 0 if missing (represents no quality rating)
        kitchen_qual_ord = safe_float(mapped_data.get('kitchen_qual_ord'), 0)  # 0 if missing
        exter_qual_ord = safe_float(mapped_data.get('exter_qual_ord'), 0)
        heating_qc_ord = safe_float(mapped_data.get('heating_qc_ord'), 0)
        bsmt_qual_ord = safe_float(mapped_data.get('bsmt_qual_ord'), 0)
        fireplace_qu_ord = safe_float(mapped_data.get('fireplace_qu_ord'), 0)  # 0 for no fireplace
        garage_finish_ord = garage_finish  # Same mapping
        
        # House style (binary: 1 if 2-story, 0 otherwise)
        house_style_2story = 1 if mapped_data.get('house_style') == '2Story' else 0
        
        # Current year for age calculations
        current_year = 2025
        
        # Calculate engineered features to match model training
        total_sf = total_bsmt_sf + first_flr_sf + second_flr_sf
        gr_liv_area = first_flr_sf + second_flr_sf  # Above ground living area
        total_sf_plus_garage = total_sf + garage_area
        total_baths = full_bath + (0.5 * half_bath)
        house_age = current_year - year_built
        remodel_age = current_year - year_remod_add
        
        # Interaction features
        qual_x_sf = overall_qual * total_sf
        qual_x_sf_plus_garage = overall_qual * total_sf_plus_garage
        garage_finish_x_garage_area = garage_finish * garage_area
        garage_finish_x_garage_area_x_garage_cars = garage_finish * garage_area * garage_cars
        garage_cars_x_garage_area = garage_cars * garage_area
        garage_finish_x_garage_cars = garage_finish * garage_cars
        
        # Create feature array in the exact order expected by the models
        feature_dict = {
            'Qual x SF Plus Garage': qual_x_sf_plus_garage,
            'Qual x SF': qual_x_sf,
            'Remodel Age': remodel_age,
            'Gr Liv Area': gr_liv_area,
            'Total SF Plus Garage': total_sf_plus_garage,
            'Year Remod/Add': year_remod_add,
            'Total Bsmt SF': total_bsmt_sf,
            'House Age': house_age,
            'Garage Yr Blt': garage_yr_blt,
            'Fireplace Qu_Ord': fireplace_qu_ord,
            'Total SF': total_sf,
            'Year Built': year_built,
            '1st Flr SF': first_flr_sf,
            'Garage Finish x Garage Area': garage_finish_x_garage_area,
            'Kitchen Qual_Ord': kitchen_qual_ord,
            'Garage Finish x Garage Area x Garage Cars': garage_finish_x_garage_area_x_garage_cars,
            'Bsmt Qual_Ord': bsmt_qual_ord,
            'Garage Cars x Garage Area': garage_cars_x_garage_area,
            'Garage Area': garage_area,
            'Garage Finish x Garage Cars': garage_finish_x_garage_cars,
            'Heating QC_Ord': heating_qc_ord,
            'Total Baths': total_baths,
            'Overall Qual': overall_qual,
            'Garage Finish_Ord': garage_finish_ord,
            'Exter Qual_Ord': exter_qual_ord,
            'House Style__2Story': house_style_2story,
            'Garage Cars': garage_cars
        }
        
        # Convert to DataFrame for sklearn models
        import pandas as pd
        feature_df = pd.DataFrame([feature_dict])
        
        return feature_df
