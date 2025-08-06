import pandas as pd
import numpy as np
import time

# Define the range for each factor
wind_range = (0, 50)  # knots
current_range = (0, 6)  # knots
wave_height_range = (0.5, 20)  # meters

# Function to generate random values within specified ranges
def generate_random_values():
    wind = np.random.uniform(*wind_range)
    current = np.random.uniform(*current_range)
    wave_height = np.random.uniform(*wave_height_range)
    return wind, current, wave_height

# Load the existing CSV file with latitudes and longitudes
input_csv = r"C:/g2/sih/ocean_points.csv"
df = pd.read_csv(input_csv)

# Create a new DataFrame to store updated data
df_updated = df.copy()
df_updated['Surface Winds (knots)'] = np.nan
df_updated['Currents (knots)'] = np.nan
df_updated['Wave Height (meters)'] = np.nan

def update_values(df):
    # Initialize previous values for smooth changes
    prev_wind, prev_current, prev_wave_height = generate_random_values()
    
    for index, row in df.iterrows():
        # Randomly assign values within the defined ranges but close to the previous values
        wind = prev_wind + np.random.uniform(-5, 5)
        current = prev_current + np.random.uniform(-1, 1)
        wave_height = prev_wave_height + np.random.uniform(-2, 2)
        
        # Ensure values stay within defined ranges
        wind = max(min(wind_range[1], wind), wind_range[0])
        current = max(min(current_range[1], current), current_range[0])
        wave_height = max(min(wave_height_range[1], wave_height), wave_height_range[0])
        
        # Update DataFrame
        df.at[index, 'Surface Winds (knots)'] = wind
        df.at[index, 'Currents (knots)'] = current
        df.at[index, 'Wave Height (meters)'] = wave_height
        
        # Update previous values
        prev_wind, prev_current, prev_wave_height = wind, current, wave_height

def save_to_csv(df, file_name):
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    while True:
        update_values(df_updated)
        save_to_csv(df_updated, r"C:\g2\updated_coordinates.csv")
        print("Updated CSV file with new values.")
        time.sleep(3)  
