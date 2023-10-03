import pandas as pd
import os
import json


def json_to_excel(directory, output_file):
    # Get a list of all JSON files in the specified directory
    json_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]

    # Create an empty DataFrame to store all the data
    combined_df = pd.DataFrame()

    # Iterate over each JSON file
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)

            # Convert the JSON data to a pandas DataFrame
            df = pd.json_normalize(data)

            # Extract and expand the list of dictionaries in columns G, H, and I
            for col in ['mlFirstHalf', 'mlSecondHalf', 'mlFullTime']:
                if col in df.columns:
                    expanded_df = pd.json_normalize(data[col])

                    # Add the additional information at the top row
                    additional_info = pd.DataFrame({
                        'homeTeam': [data['homeTeam']],
                        'awayTeam': [data['awayTeam']],
                        'date': [data['date']],
                        'day': [data['day']],
                        'leagueName': [data['leagueName']]
                    })
                    expanded_df = pd.concat([additional_info, expanded_df], ignore_index=True)

                    # Append the expanded DataFrame to the combined DataFrame
                    combined_df = pd.concat([combined_df, expanded_df], ignore_index=True)

    # Write the combined DataFrame to a single sheet in the Excel file
    combined_df.to_excel(output_file, index=False)


if __name__ == "__main__":
    directory = "F:\\Downloads\\odds-portal-scraper-main\\odds-portal-scraper-main\\data"
    output_file = "output.xlsx"

    json_to_excel(directory, output_file)
