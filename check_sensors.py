import json

import pandas as pd
import yaml


def read_settings(file):
    """
    Opens a config file and finds the max days without calibration and the output destination
    returns these two objects.
    """
    with open(file, "r") as file:
        data = yaml.safe_load(file)

        return data["max_days_since_calibration"], data["output_file"]


def read_and_join_data(xlsx, csv):
    """
    Reads a given xlsx and csv file and merges the rows in these files based on sensor id
    returns one object which is the merged data.
    """
    xlsx_d = pd.read_excel(xlsx)
    csv_d = pd.read_csv(csv, index_col=False)
    new_data = pd.merge(xlsx_d, csv_d, on="sensor_id")
    print("Merged rows:", len(new_data))
    print(new_data)
    return new_data


def handle_json(data, max_days: int, filepath):
    """
    Understood it so that just the overdue sensors should be listed.
    """
    uncalibrated_data = data[data["days_since_calibration"] > max_days]
    uncalibrated_json = uncalibrated_data.to_dict(orient="records")

    with open(filepath, "w") as fp:
        json.dump(uncalibrated_json, fp, indent=2)


handle_json(
    read_and_join_data("sensors.xlsx", "calibrations.csv"), *read_settings("config.yml")
)
