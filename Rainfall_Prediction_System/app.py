import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Rainfall Prediction System", layout="centered")

st.title("Rainfall Prediction System")
st.write("rainfall prediction project ")

states = ["Maharashtra", "Kerala", "Tamil Nadu", "Rajasthan", "Punjab"]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October']

data = []

for state in states:
    for month_index, month in enumerate(months):
        for _ in range (4) :
            if month in ["January", "July", "August", "September"] :
                rainfall = 150 + month_index * 5
                humidity = 75
                temp = 28
            else :
                rainfall = 20 + month_index * 2
                humidity = 45
                temp = 35
                
            if state == "Kerala" :
                rainfall += 40
            elif state == "Rajasthan" :
                rainfall -= 30
                
            wind_speed = 10 + month_index
            
            data.append([
                state, month, temp, humidity, wind_speed, rainfall            
                ])
            
df = pd.DataFrame(
    data,
    columns=[
        "State", "Month", "Temperature", "Humidity", "Wind Speed", "Rainfall_mm"
    ]
)

if st.checkbox ("Show dataset") :
    st.write (df.head (20))
    st.write ("Total records :",df.shape[0])
    
df_encoded = pd.get_dummies (df, drop_first=True)
X = df_encoded.drop ("Rainfall_mm", axis=1)
y = df_encoded["Rainfall_mm"]

x_train, x_test, y_train, y_test = train_test_split (
    X, y, test_size=0.2, shuffle=False
    )

model = LinearRegression()
model.fit (x_train, y_train)

st.subheader ("Enter Climate Details")

state_input = st.selectbox ("Select State", states)
month_input = st.selectbox ("Select Month", months)
temp_input = st.slider ("Temperature (°C)", min_value=0, max_value=50, value=25)
humidity_input = st.slider ("Humidity (%)", min_value=0, max_value=100, value=50)
wind_speed_input = st.slider ("Wind Speed (km/h)", min_value=0, max_value=100, value=10)

input_data = pd.DataFrame ([{
    "State" : state_input,
    "Month" : month_input,      
    "Temperature" : temp_input, 
    "Humidity" : humidity_input,    
    "Wind Speed" : wind_speed_input 
}])

input_encoded = pd.get_dummies (input_data)
input_encoded = input_encoded.reindex (columns=X.columns, fill_value=0)

if st.button ("Predict Rainfall") :
    prediction = model.predict (input_encoded)[0]
    st.success (f"Predicted Rainfall: {prediction:.2f} mm")
    
    st.write ("---")
    st.caption("Bhagirath Argade | Rainfall Prediction using Linear Regression")