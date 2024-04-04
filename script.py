import pandas as pd
import random
import os
import csv
import numpy as np

def get_consecutive_data(file, column_indices):
    try:
        data = pd.read_csv(file)  # Try reading the file as CSV
        num_rows = len(data)
        if num_rows < 30:
            print(f"Skipping file '{file}' as it does not have enough rows for consecutive data extraction.")
            return None
        start_index = random.randint(0, num_rows - 30)  # Generate a random starting index
        consecutive_data = data.iloc[start_index : start_index + 30]  # Get 30 consecutive rows for specified columns
        return consecutive_data.values.tolist()
    except pd.errors.ParserError:  # Handle the case where the file is not in CSV format
        print(f"Skipping file '{file}' as it is not in CSV format.")
        return None

def find_outliers(data):
    # Extract prices from data
    prices = [item[2] for item in data]

    # Calculate quartiles
    Q1 = np.percentile(prices, 25)
    Q3 = np.percentile(prices, 75)

    # Calculate interquartile range (IQR)
    IQR = Q3 - Q1

    # Determine lower and upper bounds
    lower_bound = Q1 - .5 * IQR
    upper_bound = Q3 + .5* IQR

    # Identify outliers
    outliers = [item for item in data if item[2] < lower_bound or item[2] > upper_bound]

    return outliers

# Get current path
current_directory = os.getcwd()

# Retrieve all items from the current directory
all_items = os.listdir(current_directory)

# Filter to obtain only directories
directory_list = [item for item in all_items if os.path.isdir(os.path.join(current_directory, item))]

print("List of directories in the current directory:")
for i, directory in enumerate(directory_list):
    print(f"{i+1}. {directory}")

directory_index = int(input("Select a directory number from the list: ")) - 1

if directory_index >= 0 and directory_index < len(directory_list):
    selected_directory = directory_list[directory_index]
    print(f"You selected directory: {selected_directory}")

    # Filter to obtain only directories
    selected_directory_path = os.path.join(current_directory, selected_directory)
    selected_directory_items = os.listdir(selected_directory_path)

    # Filter to obtain only files without "_outliers" in their names
    file_list = [item for item in selected_directory_items if os.path.isfile(os.path.join(selected_directory_path, item)) and "_outliers" not in item]

    print("List of files in the selected directory:")
    for i, file in enumerate(file_list):
        print(f"{i+1}. {file}")

    for file_index, selected_file in enumerate(file_list):
        print(f"Processing file {file_index + 1}/{len(file_list)}: {selected_file}")
        if selected_file.endswith('.csv'):  # Check if the file has a CSV extension
            column_indices = [2]
            consecutive_data = get_consecutive_data(os.path.join(selected_directory_path, selected_file),column_indices)
            if consecutive_data is not None:
                #print(consecutive_data)

                # Identify outliers
                outliers = find_outliers(consecutive_data)
                #print("Outliers:")
                #print(outliers)

                filename = os.path.join(selected_directory_path, os.path.splitext(selected_file)[0] + "_outliers.csv")
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(outliers)

                print(f"The result has been written to the file '{filename}'.")
        else:
            print(f"Skipping file '{selected_file}' as it is not a CSV file.")

else:
    print("The selected directory number is not valid")
