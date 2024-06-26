import streamlit as st
import pandas as pd
import pickle

# Dictionary to store model paths and corresponding input features for each tool
tools_info = {
    "Boss": {"model_path": "./Saved Model/Boss.pkl",
             "input_features": ['Material Type [Aluminimum Alloy - 1]',
                                'Material Hardness Number[Rockwell]',
                                'Density [Kg/m³]',
                                'Poissons Ratio',
                                'Length[mm] {Range : 3 - 30}',
                                'Diameter[mm] {Range : 0 - 18}',
                                'Tolerance[mm]',
                                'Surface finish[mm]'],
             "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Chamfer": {"model_path": "./Saved Model/Chamfer.pkl",
                "input_features": ['Material Type [Aluminimum Alloy - 1]',
                                   'Material Hardness Number[Rockwell]',
                                   'Density [Kg/m³]',
                                   'Poissons Ratio',
                                   'Length[mm]{Range : 6 - 10}',
                                   'Angle {Range : 25° - 45°}',
                                   'Tolerance[mm]',
                                   'Surface finish[mm]'],
                "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Fillet": {"model_path": "./Saved Model/Fillet.pkl",
               "input_features": ['Material Type [Aluminimum Alloy - 1]',
                                  'Material Hardness Number[Rockwell]',
                                  'Density [Kg/m³]',
                                  'Poissons Ratio',
                                  'Radius[mm]{Range : 0 - 6}',
                                  'Tolerance[mm]',
                                  'Surface finish[mm]'],
               "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Hole": {"model_path": "./Saved Model/Hole.pkl",
             "input_features": ['Material Type [Aluminimum Alloy - 1]',
                                'Material Hardness Number[Rockwell]',
                                'Density [Kg/m³]',
                                'Poissons Ratio',
                                'Diameter[mm]{Range : 0 - 10}',
                                'Depth[mm]{Range : 0 - 20}',
                                'Tolerance[mm]',
                                'Surface finish[mm]'],
             "output_headings": ['Drilling', 'Reaming', 'Finish Reaming operation', 'Rough Boring', 'Finish boring']},
    
    "Pocket": {"model_path": "./Saved Model/Pocket.pkl",
               "input_features": ['Material Type [Aluminimum Alloy - 1]',
                                  'Material Hardness Number[Rockwell]',
                                  'Density [Kg/m³]',
                                  'Poissons Ratio',
                                  'Length[mm]{Range : 3 - 80}',
                                  'Depth[mm]{Range : 0 - 20}',
                                  'Width[mm]{Range : 3 - 80}',
                                  'Tolerance[mm]',
                                  'Surface finish[mm]'],
               "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Step": {"model_path": "./Saved Model/Step.pkl",
             "input_features": ['Material Type [Aluminimum Alloy - 1]',
                                'Material Hardness Number[Rockwell]',
                                'Density [Kg/m³]',
                                'Poissons Ratio',
                                'Length[mm]{Range : 10 - 100}',
                                'Depth[mm]{Range : 6 - 10}',
                                'Width[mm]{Range : 10 - 100}',
                                'Tolerance[mm]',
                                'Surface finish[mm]'],
             "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']}
}

# Define the mapping between scientific tolerance values and their numeric ranges for each tool
tolerance_to_numeric_range = {
    'Boss': {
        'IT11 - IT13': '0.6 - 0.33',
        'IT8 - IT11': '0.014 -  0.06',
        'IT3 - IT8': '0.0020 - 0.014',
    },
    'Chamfer': {
        'IT11 - IT13': '0.09 - 0.22',
        'IT8 - IT11': '0.022 -  0.09',
        'IT3 - IT8': '0.0025 - 0.022',
    },
    'Fillet': {
        'IT11 - IT13': '0.06 - 0.18',
        'IT8 - IT11': '0.014 -  0.06',
        'IT3 - IT8': '0.0020 - 0.014',
    },
    'Hole': {
        'IT11 - IT13': '0.06 - 0.27',
        'IT7': '0.01 -  0.018',
        'IT12 - IT13': '0.10 - 0.27',
        'IT7 - IT9': '0.01 - 0.043',
    },
    'Pocket': {
        'IT11 - IT13': '0.075 - 0.46',
        'IT8 - IT11': '0.018 -  0.075',
        'IT3 - IT8': '0.0025 - 0.018',
    },
    'Step': {
        'IT11 - IT13': '0.09 - 0.54',
        'IT8 - IT11': '0.022 -  0.09',
        'IT3 - IT8': '0.0025 - 0.022',
    }
}

# Define the corresponding surface finish ranges for each tool
tolerance_to_surface_finish = {
    'Boss': {
        'IT11 - IT13': '0.01 - 0.020',
        'IT8 - IT11': '0.00125 - 0.010',
        'IT3 - IT8': '0.000325 - 0.00125',
    },
    'Chamfer': {
        'IT11 - IT13': '0.01 - 0.020',
        'IT8 - IT11': '0.00125 - 0.010',
        'IT3 - IT8': '0.00032 - 0.00125',
    },
    'Fillet': {
        'IT11 - IT13': '0.01 - 0.020',
        'IT8 - IT11': '0.00125 - 0.010',
        'IT3 - IT8': '0.00032 - 0.00125',
    },
    'Hole': {
        'IT11 - IT13': '0.005 - 0.08',
        'IT7': '0.0008 - 0.0016',
        'IT12 - IT13': '0.005 - 0.02',
        'IT7 - IT9': '0.00062 - 0.0025',
    },
    'Pocket': {
        'IT11 - IT13': '0.01 - 0.020',
        'IT8 - IT11': '0.00125 -  0.010',
        'IT3 - IT8': '0.000325 - 0.00125',
    },
    'Step': {
        'IT11 - IT13': '0.01 - 0.020',
        'IT8 - IT11': '0.00125 -  0.010',
        'IT3 - IT8': '0.00032 - 0.00125',
    }
}

# Function to load models
def load_models(tools_info):
    loaded_models = {}
    for tool, info in tools_info.items():
        try:
            with open(info["model_path"], 'rb') as file:
                loaded_models[tool] = pickle.load(file)
        except Exception as e:
            st.error(f"Error loading model for {tool}: {e}")
    return loaded_models

# Load models
loaded_models = load_models(tools_info)

# Function to make predictions for a tool's operation
def predict_operation(input_data, model):
    try:
        predictions = model.predict(input_data)
        return predictions
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

# Function to handle input data collection
def collect_input_data(tool, features):
    tool_input_data = {}
    input_valid = True
    for feature in features:
        if feature == 'Material Type [Aluminimum Alloy - 1]':
            tool_input_data[feature] = st.selectbox(f"{feature}:", ['1'], key=f"{tool}_{feature}")
        elif feature == 'Material Hardness Number[Rockwell]':
            tool_input_data[feature] = st.selectbox(f"{feature}:", ['35.45'], key=f"{tool}_{feature}")
        elif feature == 'Density [Kg/m³]':
            tool_input_data[feature] = st.selectbox(f"{feature}:", ['2870'], key=f"{tool}_{feature}")
        elif feature == 'Poissons Ratio':
            tool_input_data[feature] = st.selectbox(f"{feature}:", ['0.26'], key=f"{tool}_{feature}")
            
        elif feature == 'Length[mm] {Range : 3 - 30}' and tool == "Boss":
            value = st.number_input(f"{feature}:", min_value=3, max_value=30, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
        elif feature == 'Diameter[mm] {Range : 0 - 18}' and tool == "Boss":
            value = st.number_input(f"{feature}:", min_value=0, max_value=18, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
            
        elif feature == 'Length[mm]{Range : 6 - 10}' and tool == "Chamfer":
            value = st.number_input(f"{feature}:", min_value=6, max_value=10, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
        elif feature == 'Angle {Range : 25° - 45°}' and tool == "Chamfer":
            value = st.number_input(f"{feature}:", min_value=25, max_value=45, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
            
        elif feature == 'Radius[mm]{Range : 0 - 6}' and tool == "Fillet":
            value = st.number_input(f"{feature}:", min_value=0, max_value=6, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
            
        elif feature == 'Diameter[mm]{Range : 0 - 10}' and tool == "Hole":
            value = st.number_input(f"{feature}:", min_value=0, max_value=10, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
        elif feature == 'Depth[mm]{Range : 0 - 20}' and tool == "Hole":
            value = st.number_input(f"{feature}:", min_value=0, max_value=20, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
            
        elif feature == 'Length[mm]{Range : 3 - 80}' and tool == "Pocket":
            value = st.number_input(f"{feature}:", min_value=3, max_value=80, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
        elif feature == 'Depth[mm]{Range : 0 - 20}' and tool == "Pocket":
            value = st.number_input(f"{feature}:", min_value=0, max_value=20, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
        elif feature == 'Width[mm]{Range : 3 - 80}' and tool == "Pocket":
            value = st.number_input(f"{feature}:", min_value=3, max_value=80, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
            
        elif feature == 'Length[mm]{Range : 10 - 100}' and tool == "Step":
            value = st.number_input(f"{feature}:", min_value=10, max_value=100, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
        elif feature == 'Depth[mm]{Range : 6 - 10}' and tool == "Step":
            value = st.number_input(f"{feature}:", min_value=6, max_value=10, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
        elif feature == 'Width[mm]{Range : 10 - 100}' and tool == "Step":
            value = st.number_input(f"{feature}:", min_value=10, max_value=100, key=f"{tool}_{feature}")
            tool_input_data[feature] = value
            
        elif feature not in ['Tolerance[mm]', 'Surface finish[mm]']:
            tool_input_data[feature] = st.text_input(f"{feature}:", key=f"{tool}_{feature}")
    
    # Select tolerance range
    tolerance_range = st.selectbox("Select Tolerance Range:", list(tolerance_to_numeric_range[tool].keys()), key=f"{tool}_tolerance_range")
    numeric_tolerance_range = tolerance_to_numeric_range[tool][tolerance_range]
    tolerance_value = st.number_input(f"Tolerance[mm] (Range: {numeric_tolerance_range}):", key=f"{tool}_tolerance_value", format="%.3f")
    
    if not (float(numeric_tolerance_range.split('-')[0]) <= tolerance_value <= float(numeric_tolerance_range.split('-')[1])):
        st.error(f"Tolerance must be within the range {numeric_tolerance_range}")
        input_valid = False
    else:
        tool_input_data['Tolerance[mm]'] = tolerance_value
        surface_finish_range = tolerance_to_surface_finish[tool][tolerance_range]
        st.write(f"Corresponding Surface Finish Range: {surface_finish_range}")
        surface_finish_value = st.number_input(f"Surface finish[mm] (Range: {surface_finish_range}):", key=f"{tool}_surface_finish_value", format="%.4f")
        
        if not (float(surface_finish_range.split('-')[0]) <= surface_finish_value <= float(surface_finish_range.split('-')[1])):
            st.error(f"Surface finish must be within the range {surface_finish_range}")
            input_valid = False
        else:
            tool_input_data['Surface finish[mm]'] = surface_finish_value

    return tool_input_data if input_valid else None

def main():
    st.title("Machining Operations Prediction")

    st.sidebar.header("Select Tool")
    selected_tools = st.sidebar.multiselect("Select Feature:", list(tools_info.keys()))
    
    input_data = {}
    for tool in selected_tools:
        with st.expander(f"Enter the input data for {tool}:"):
            input_data[tool] = collect_input_data(tool, tools_info[tool]["input_features"])

    if st.button("Predict"):
        for tool, tool_input_data in input_data.items():
            if tool_input_data:
                input_df = pd.DataFrame([tool_input_data])
                predictions = predict_operation(input_df, loaded_models[tool])
                if predictions is not None:
                    st.write(f"Predicted Operations for {tool}:")
                    for i in range(len(predictions[0])):
                        st.write(f"{tools_info[tool]['output_headings'][i]}: {predictions[0][i]}")

if __name__ == "__main__":
    main()
