
# Import necessary libraries
import joblib                      # For loading the serialized model
import pandas as pd                # For data manipulation
from flask import Flask, request, jsonify

# Initialize the Flask application
sales_prediction_api = Flask("SuperKart Sales Prediction API")

# Load the trained machine learning model
model = joblib.load("superkart_sales_prediction_model_v1.joblib")


# Define a route for the home page (GET request)
@sales_prediction_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/').
    It returns a welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"


# Define an endpoint for single prediction (POST request)
@sales_prediction_api.post('/v1/sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing product details and returns
    the predicted sales.
    """

    # Get JSON data
    product_data = request.get_json()

    # Extract required features
    sample = {
        "Product_Weight": product_data["Product_Weight"],
        "Product_Allocated_Area": product_data["Product_Allocated_Area"],
        "Product_MRP": product_data["Product_MRP"],
        "Store_Establishment_Year": product_data["Store_Establishment_Year"],
        "Product_Id": product_data["Product_Id"],
        "Product_Sugar_Content": product_data["Product_Sugar_Content"],
        "Product_Type": product_data["Product_Type"],
        "Store_Id": product_data["Store_Id"],
        "Store_Size": product_data["Store_Size"],
        "Store_Location_City_Type": product_data["Store_Location_City_Type"],
        "Store_Type": product_data["Store_Type"]
    }

    # Convert input into DataFrame
    input_data = pd.DataFrame([sample])

    # Predict sales
    predicted_sales = model.predict(input_data)[0]

    # Convert NumPy float to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # Return prediction
    return jsonify({
        "Predicted Product Store Sales": predicted_sales
    })


# Define an endpoint for batch prediction (POST request)
@sales_prediction_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing multiple products and returns
    predicted sales.
    """

    # Read uploaded CSV
    file = request.files["file"]
    input_data = pd.read_csv(file)

    # Predict sales
    predicted_sales = model.predict(input_data).tolist()

    # Convert NumPy floats to Python floats
    predicted_sales = [round(float(x), 2) for x in predicted_sales]

    # Create output dictionary
    product_ids = input_data["Product_Id"].tolist()
    output_dict = dict(zip(product_ids, predicted_sales))

    return output_dict


# Run the Flask application
if __name__ == "__main__":
    sales_prediction_api.run(debug=True)
