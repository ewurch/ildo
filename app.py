# app.py
from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__, template_folder='templates')

def load_data(file):
    # Load CSV or Excel file
    return pd.read_csv(file)  # Adjust as needed for Excel

def basic_analysis(df):
    # Perform basic statistical analysis
    return df.describe().to_dict()

def engineer_features(df):
    # Implement basic feature engineering methods
    numeric_features = df.select_dtypes(include=[np.number]).columns
    categorical_features = df.select_dtypes(include=['object']).columns
    
    # Polynomial features
    poly = PolynomialFeatures(degree=2, include_bias=False)
    poly_features = poly.fit_transform(df[numeric_features])
    poly_feature_names = poly.get_feature_names_out(numeric_features)
    
    # One-hot encoding
    onehot = OneHotEncoder(sparse=False)
    onehot_features = onehot.fit_transform(df[categorical_features])
    onehot_feature_names = onehot.get_feature_names(categorical_features)
    
    # Combine all features
    all_features = np.hstack((poly_features, onehot_features))
    all_feature_names = np.concatenate((poly_feature_names, onehot_feature_names))
    
    return pd.DataFrame(all_features, columns=all_feature_names)

def select_features(df, k=10):
    # Simple feature selection using variance threshold
    selector = VarianceThreshold()
    selected_features = selector.fit_transform(df)
    selected_feature_names = df.columns[selector.get_support()]
    return selected_features[:, :k], selected_feature_names[:k]

def train_model(X, y):
    # Train a simple linear regression model
    model = LinearRegression()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return model, mse, r2

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = load_data(file)
        analysis = basic_analysis(df)
        engineered_features = engineer_features(df)
        selected_features, feature_names = select_features(engineered_features)
        
        # Assuming the last column is the target variable
        target = df.iloc[:, -1]
        model, mse, r2 = train_model(selected_features, target)
        
        return jsonify({
            'analysis': analysis,
            'selected_features': feature_names.tolist(),
            'model_performance': {
                'mse': mse,
                'r2': r2
            }
        })
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)