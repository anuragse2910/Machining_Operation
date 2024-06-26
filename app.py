import streamlit as st
import pandas as pd
import pickle

# Dictionary to store model paths and corresponding input features for each tool
tools_info = {
    "Boss": {"model_path": "./Saved Model/Boss.pkl",
            "input_features": ['Material Type [Aluminimum Alloy - 1]', 'Material Hardness Number[Rockwell]', 'Desity [Kg/m³]', 'Poissons Ratio', 'Length[mm]', 'Diameter[mm]', 'Tolerance[mm]','Surface finish[mm]' ],
            "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Chamfer": {"model_path": "./Saved Model/Chamfer.pkl",
            "input_features": ['Material Type [Aluminimum Alloy - 1]', 'Material Hardness Number[Rockwell]', 'Desity [Kg/m³]', 'Poissons Ratio', 'Length[mm]', 'Angle', 'Tolerance[mm]','Surface finish[mm]'],
            "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Fillet": {"model_path": "./Saved Model/Fillet.pkl",
            "input_features": ['Material Type [Aluminimum Alloy - 1]', 'Material Hardness Number[Rockwell]', 'Desity [Kg/m³]', 'Poissons Ratio', 'Radius[mm]', 'Tolerance[mm]','Surface finish[mm]'],
            "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Hole": {"model_path": "./Saved Model/Hole.pkl",
            "input_features": ['Material Type [Aluminimum Alloy - 1]', 'Material Hardness Number[Rockwell]', 'Desity [Kg/m³]', 'Poissons Ratio', 'Diameter[mm]', 'Depth[mm]', 'Tolerance[mm]','Surface finish[mm]'],
            "output_headings": ['Drilling', 'Reaming', 'Finish Reaming operation','Rough Boring','Finish boring']},
    
    "Pocket": {"model_path": "./Saved Model/Pocket.pkl",
            "input_features": ['Material Type [Aluminimum Alloy - 1]', 'Material Hardness Number[Rockwell]', 'Desity [Kg/m³]', 'Poissons Ratio', 'Length[mm]', 'Depth[mm]','Width[mm]', 'Tolerance[mm]','Surface finish[mm]'],
            "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']},
    
    "Step": {"model_path": "./Saved Model/Step.pkl",
            "input_features": ['Material Type [Aluminimum Alloy - 1]', 'Material Hardness Number[Rockwell]', 'Desity [Kg/m³]', 'Poissons Ratio', 'Length[mm]', 'Depth[mm]','Width[mm]', 'Tolerance[mm]','Surface finish[mm]'],
            "output_headings": ['End Milling-Rough operation', 'End Milling-Semi finish operation', 'End Milling-Finish operation']}
}

# Function to load models
def load_models(tools_info):
    loaded_models = {}
    for tool, info in tools_info.items():
        with open(info["model_path"], 'rb') as file:
            loaded_models[tool] = pickle.load(file)
    return loaded_models

# Load models
loaded_models = load_models(tools_info)

# Function to make predictions for a tool's operation
def predict_operation(input_data, model):
    # Make predictions on the input data using the specified model
    predictions = model.predict(input_data)
    return predictions

def main():
    st.title("Machining Operations Prediction")

    # multiselected tool widget
    # Add a sidebar with a select feature
    st.sidebar.header("Select Tool")
    selected_tool = st.sidebar.multiselect("Select Feature:", list(tools_info.keys()))
    
    #creating a container to display the selected tools' input features
    container = st.container()

    # Create a dictionary to store the input data for each selected tool
    input_data = {}

    # Loop through the selected tools
    for tool in selected_tool:
        with container:
            st.write(f"Enter the input data for {tool}:")
            tool_input_data = {}
            for feature in tools_info[tool]["input_features"]:
                if feature == 'Material Type [Aluminimum Alloy - 1]':
                    material_type_options = ['1']
                    tool_input_data[feature]= st.selectbox(f"{feature}:", material_type_options, key=f"{tool}_{feature}")
                elif feature == 'Material Hardness Number[Rockwell]':
                    hardness_options = ['35.45']
                    tool_input_data[feature] = st.selectbox(f"{feature}:", hardness_options, key=f"{tool}_{feature}")
                
                elif feature == 'Desity [Kg/m³]':
                        density_options = ['2700']
                        tool_input_data[feature] = st.selectbox(f"{feature}:", density_options, key=f"{tool}_{feature}")
                elif feature == 'Poissons Ratio':
                    poissons_options = ['0.26']
                    tool_input_data[feature] = st.selectbox(f"{feature}:", poissons_options, key=f"{tool}_{feature}")
                else:
                    tool_input_data[feature] = st.text_input(f"{feature}:", key=f"{tool}_{feature}")
            input_data[tool] = tool_input_data

    if st.button("Predict"):
        for tool, tool_input_data in input_data.items():
            input_df = pd.DataFrame([tool_input_data])
            # Create a pandas DataFrame
            predictions = predict_operation(input_df, loaded_models[tool])
            st.write(f"Predicted Operations for {tool}:")
            for i, heading in enumerate(tools_info[tool]["output_headings"]):
                st.write(f"{heading}: {predictions[0][i]}")

if __name__ == "__main__":
    main()