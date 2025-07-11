class PricingEngine:
    def __init__(self):
        self.model = None
        self.data = None

    def load_data(self, file_path):
        import pandas as pd
        self.data = pd.read_csv(file_path)

    def train_model(self):
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression

        if self.data is None:
            raise ValueError("Data not loaded. Please load data before training the model.")

        X = self.data.drop('price', axis=1)
        y = self.data['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        return self.model.score(X_test, y_test)

    def predict_price(self, features):
        if self.model is None:
            raise ValueError("Model not trained. Please train the model before making predictions.")

        import numpy as np
        features_array = np.array(features).reshape(1, -1)
        return self.model.predict(features_array)[0]
