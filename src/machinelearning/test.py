import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC


def train_model(csv_file, target_var, save_path='models/'):
    data = pd.read_csv(csv_file)

    imputer = SimpleImputer(strategy='mean')
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    data[numeric_cols] = imputer.fit_transform(data[numeric_cols])

    for col in data.select_dtypes(include=['object']).columns:
        if col != target_var:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])

    X = data.drop(target_var, axis=1)
    y = data[target_var]

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'LogisticRegression': LogisticRegression(),
        'SVC': SVC(probability=True),
        'RandomForestClassifier': RandomForestClassifier()
    }

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'{model_name} Accuracy: {accuracy:.2f}')

        with open(f'{save_path}{model_name}.pkl', 'wb') as file:
            pickle.dump(model, file)

    with open(f'{save_path}scaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)

    with open(f'{save_path}imputer.pkl', 'wb') as file:
        pickle.dump(imputer, file)

    print('Models, scaler, and imputer saved successfully.')


def load_model_and_predict_with_imputation(model_path, scaler_path, imputer_path):
    with open(model_path, 'rb') as model_file:
        rfc_model = pickle.load(model_file)

    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    with open(imputer_path, 'rb') as imputer_file:
        imputer = pickle.load(imputer_file)

    print("Model, scaler, and imputer loaded successfully.")

    print("Enter the feature values for prediction (type 'nan' for missing values):")
    input_values = [4.9, 3, 1.4, .2]

    input_values = np.array(input_values).reshape(1, -1)

    input_values_imputed = imputer.transform(input_values)

    input_values_scaled = scaler.transform(input_values_imputed)

    prediction = rfc_model.predict(input_values_scaled)
    prediction_proba = rfc_model.predict_proba(input_values_scaled)

    print(f"Prediction: {prediction[0]}")
    print(f"Prediction Probabilities: {prediction_proba[0]}")
