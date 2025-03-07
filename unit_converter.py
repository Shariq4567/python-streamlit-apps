import streamlit as st

def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        'meters': 1.0,
        'kilometers': 0.001,
        'centimeters': 100,
        'millimeters': 1000,
        'miles': 0.000621371,
        'yards': 1.09361,
        'feet': 3.28084,
        'inches': 39.3701,
        }
    
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        return None
    
    value_in_base = value / conversion_factors[from_unit]
    converted_value = value_in_base * conversion_factors[to_unit]
    return converted_value

st.title('Unit Converter')

value = st.number_input('Enter the value to convert:', min_value=0.0, format="%.2f")
from_unit = st.selectbox('From unit:', ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'yards', 'feet', 'inches'])
to_unit = st.selectbox('To unit:', ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'yards', 'feet', 'inches'])

if st.button('Convert'):
    result = convert_units(value, from_unit, to_unit)
    if result is not None:
        st.write(f'{value} {from_unit} is equal to {result:.2f} {to_unit}')
    else:
        st.write('Invalid unit conversion')