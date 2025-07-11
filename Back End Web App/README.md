# House Pricing API

This project is a Flask web application that provides a RESTful API for pricing houses using machine learning techniques. It utilizes libraries such as NumPy, Pandas, Matplotlib, and SciPy to build a pricing engine that can predict house prices based on various input features.

## Project Structure

```
back end web app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── services
│   │   ├── __init__.py
│   │   └── pricing_engine.py
│   ├── models
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
├── tests
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_pricing_engine.py
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd "back end web app"
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

- `POST /predict`: Accepts input features for a house and returns the predicted price.
- `GET /priceRequest`: Accepts house feature parameters as query string and returns a response object containing the same fields, the generated price, and an optional message.

## Testing

To run the tests, use the following command:

```bash
pytest
```

## Dependencies

This project requires the following Python packages:

- Flask
- NumPy
- Pandas
- Matplotlib
- SciPy

## License

This project is licensed under the MIT License.