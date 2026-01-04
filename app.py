import streamlit as st
import pandas as pd
import joblib
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. LOAD CONFIGURATION
# Load the secret .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check if key exists
if not api_key:
    st.error("❌ API Key missing! Make sure you created the .env file.")
    st.stop()

# Configure Google Gemini
genai.configure(api_key=api_key)

# 2. LOAD THE TRAINED MODEL
# We use @st.cache_resource so we don't reload the model every time the user clicks a button (makes it faster)
@st.cache_resource
def load_resources():
    model = joblib.load('models/greenkart_xgb.pkl')
    cols = joblib.load('models/model_columns.pkl')
    return model, cols

try:
    model, model_columns = load_resources()
except FileNotFoundError:
    st.error("❌ Model files not found! Did you run the notebook in Stage 1?")
    st.stop()

# 3. THE UI LAYOUT
st.set_page_config(page_title="GreenKart AI", page_icon="🌱")
st.title("🌱 GreenKart: AI Sustainability Auditor")
st.markdown("Predict your product's carbon footprint and get **GenAI-powered recommendations**.")

# Create two columns for a clean layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Product Specs")
    material = st.selectbox("Material Type", ['Plastic', 'Glass', 'Paper', 'Metal', 'Bamboo'])
    weight = st.number_input("Weight (kg)", min_value=0.1, max_value=50.0, value=1.5)
    distance = st.number_input("Transport Distance (km)", min_value=10, max_value=5000, value=500)
    
    st.write("---")
    recyclable_input = st.radio("Is it Recyclable?", ["No", "Yes"])
    is_recyclable = 1 if recyclable_input == "Yes" else 0
    
    energy_rating = st.selectbox("Energy Efficiency Class", ['A', 'B', 'C', 'D'])

# 4. PREDICTION LOGIC
if st.button("🚀 Analyze Impact"):
    # Step A: Create a raw dataframe from user inputs
    input_data = pd.DataFrame({
        'weight_kg': [weight],
        'transport_distance_km': [distance],
        'is_recyclable': [is_recyclable],
    })

    # Step B: Handle One-Hot Encoding (The Trick!)
    # We created dummy columns in training (e.g., 'material_type_Plastic').
    # We must replicate that structure here.
    
    # Get all possible missing columns from the training phase (filled with 0)
    # This creates a dataframe with 0s for all columns the model expects
    missing_cols = set(model_columns) - set(input_data.columns)
    for c in missing_cols:
        input_data[c] = 0
        
    # Now set the specific user choice to 1
    # Example: If user chose "Plastic", we find column 'material_type_Plastic' and set to 1
    if f'material_type_{material}' in input_data.columns:
        input_data[f'material_type_{material}'] = 1
    
    if f'energy_efficiency_rating_{energy_rating}' in input_data.columns:
        input_data[f'energy_efficiency_rating_{energy_rating}'] = 1

    # Reorder columns to match exactly what the model saw during training
    input_data = input_data[model_columns]

    # Step C: Predict
    prediction = model.predict(input_data)[0]
    
    # 5. DISPLAY RESULTS & GEMINI ADVICE
    with col2:
        st.subheader("🌍 Analysis Result")
        
        # Color code the score
        if prediction > 75:
            st.success(f"Eco Score: {prediction:.1f}/100 (Excellent)")
        elif prediction > 50:
            st.warning(f"Eco Score: {prediction:.1f}/100 (Needs Improvement)")
        else:
            st.error(f"Eco Score: {prediction:.1f}/100 (High Impact!)")
            
        st.divider()
        
        st.subheader("🤖 AI Consultant Recommendations")
        with st.spinner("Consulting with Gemini API..."):
            # Construct the prompt
            prompt = f"""
            Act as a Senior Supply Chain Sustainability Officer.
            I have a product with these specs:
            - Material: {material}
            - Weight: {weight} kg
            - Transport: {distance} km
            - Recyclable: {recyclable_input}
            - Energy Rating: {energy_rating}
            
            Our predictive model gave it an Eco Score of {prediction:.1f}/100.
            
            Provide 3 specific, actionable steps to improve this score. 
            Focus on material alternatives or logistics optimization.
            Keep it concise and professional.
            """
            
            try:
                model_genai = genai.GenerativeModel('gemini-2.5-flash-lite')
                response = model_genai.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI Connection Failed: {e}")