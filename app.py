from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model and scaler
model = pickle.load(open('Medical_Inssurance_predictor.pkl','rb'))
scaler = pickle.load(open('scaling.pkl','rb'))


@app.route('/')
def home():
    return "Welcome to the Insurance Cost Prediction API!"


@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.json  # Expecting JSON input

    # Example: {"age": 31, "sex": 1, "bmi": 36.3, "children": 2, "smoker": 1}
    try:
        input_data = [
            data['age'], data['sex'], data['bmi'],
            data['children'], data['smoker']
        ]
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400

    # Convert to DataFrame with proper feature names
    feature_names = ['age', 'sex', 'bmi', 'children', 'smoker']
    input_data_as_dataframe = pd.DataFrame([input_data], columns=feature_names)

    # Scale the data
    scaled_data = scaler.transform(input_data_as_dataframe)

    # Make prediction
    prediction = model.predict(scaled_data)
    return jsonify({
        "prediction": prediction[0],
        "message": f"The predicted insurance cost is USD {prediction[0]:.2f}"
    })


if __name__ == '__main__':
    app.run(debug=True)