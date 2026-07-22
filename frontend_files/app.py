
# Import necessary libraries
import streamlit as st
import pandas as pd
import requests

# Title of the web application
st.title("🛒 SuperKart Sales Prediction")

st.write(
    """
    Predict the sales of a product based on its characteristics
    using the trained XGBoost model.
    """
)

# Backend API URL
model_root_url = "http://127.0.0.1:7860"
model_url = model_root_url + "/v1/sales"
model_batch_url = model_root_url + "/v1/salesbatch"

# Sidebar navigation
option = st.sidebar.selectbox(
    "Select Prediction Type",
    ("Single Prediction", "Batch Prediction")
)

##########################################################
# Single Prediction
##########################################################

if option == "Single Prediction":

    st.header("Enter Product Details")

    Product_Weight = st.number_input("Product Weight", value=12.5)

    Product_Allocated_Area = st.number_input(
        "Product Allocated Area",
        value=0.065,
        format="%.3f"
    )

    Product_MRP = st.number_input("Product MRP", value=249.81)

    Store_Establishment_Year = st.number_input(
        "Store Establishment Year",
        value=2007
    )

    Product_Id = st.text_input("Product ID", value="FDX07")

    Product_Sugar_Content = st.selectbox(
        "Product Sugar Content",
        ["Low Sugar", "Regular"]
    )

    Product_Type = st.text_input(
        "Product Type",
        value="Fruits and Vegetables"
    )

    Store_Id = st.text_input(
        "Store ID",
        value="OUT049"
    )

    Store_Size = st.selectbox(
        "Store Size",
        ["Small", "Medium", "High"]
    )

    Store_Location_City_Type = st.selectbox(
        "Store Location City Type",
        ["Tier 1", "Tier 2", "Tier 3"]
    )

    Store_Type = st.selectbox(
        "Store Type",
        [
            "Supermarket Type1",
            "Supermarket Type2",
            "Supermarket Type3",
            "Grocery Store"
        ]
    )

    if st.button("Predict Sales"):

        payload = {
            "Product_Weight": Product_Weight,
            "Product_Allocated_Area": Product_Allocated_Area,
            "Product_MRP": Product_MRP,
            "Store_Establishment_Year": Store_Establishment_Year,
            "Product_Id": Product_Id,
            "Product_Sugar_Content": Product_Sugar_Content,
            "Product_Type": Product_Type,
            "Store_Id": Store_Id,
            "Store_Size": Store_Size,
            "Store_Location_City_Type": Store_Location_City_Type,
            "Store_Type": Store_Type
        }

        response = requests.post(model_url, json=payload)

        if response.status_code == 200:
            prediction = response.json()

            st.success(
                f"Predicted Sales: {prediction['Predicted Product Store Sales']}"
            )
        else:
            st.error("Prediction failed.")

##########################################################
# Batch Prediction
##########################################################

else:

    st.header("Batch Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        files = {"file": uploaded_file}

        response = requests.post(
            model_batch_url,
            files=files
        )

        if response.status_code == 200:

            predictions = response.json()

            prediction_df = pd.DataFrame(
                predictions.items(),
                columns=["Product_Id", "Predicted Sales"]
            )

            st.dataframe(prediction_df)

        else:
            st.error("Batch prediction failed.")
