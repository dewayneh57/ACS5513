"""
Basic tests for the Backend Web Application
"""
import pytest
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_app_creation():
    """Test that the Flask app can be created without errors"""
    try:
        from app import create_app
        app = create_app()
        assert app is not None
        assert app.config is not None
    except Exception as e:
        pytest.fail(f"Failed to create app: {e}")

def test_pricing_engine_import():
    """Test that the pricing engine can be imported"""
    try:
        from app.services.pricing_engine import PricingEngine
        engine = PricingEngine()
        assert engine is not None
        assert hasattr(engine, 'models')
    except Exception as e:
        pytest.fail(f"Failed to import PricingEngine: {e}")

def test_routes_import():
    """Test that routes can be imported"""
    try:
        from app import routes
        assert routes is not None
    except Exception as e:
        pytest.fail(f"Failed to import routes: {e}")

if __name__ == "__main__":
    test_app_creation()
    test_pricing_engine_import() 
    test_routes_import()
    print("All tests passed!")
