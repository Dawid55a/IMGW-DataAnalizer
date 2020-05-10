import os
from pathlib import Path
import pandas as pd
from pprint import pprint

# listing all files
files = os.listdir(f"{Path.home()}/Downloads/IMGWDataDownload/Extracted")
# pprint(files)

columns = [
    "Station_code",
    "Station_name",
    "Year",
    "Month",
    "Day",
    "Daily_rainfall_sum_[mm]",
    "SMBD_measurement_status",
    "Type_of_precipitation",
    "Snow_height_[cm]",
    "PKSN_measurement_status",
    "Height_of_freshly_fallen_snow_[cm]",
    "HSS_measurement_status",
    "Snow_species",
    "GATS_measurement_status",
    "Type_of_snow_cover",
    "RPSN_measurement_status"]

data = pd.DataFrame(columns=columns)
i = 0
length = len(files)
# print(data)
for file in files:
    csv_data = pd.read_csv(f"{Path.home()}/Downloads/IMGWDataDownload/Extracted/{files[0]}", encoding='ISO-8859-2',
                           header=None)

    csv_data.rename(columns={
        0: "Station_code",
        1: "Station_name",
        2: "Year",
        3: "Month",
        4: "Day",
        5: "Daily_rainfall_sum_[mm]",
        6: "SMBD_measurement_status",
        7: "Type_of_precipitation",
        8: "Snow_height_[cm]",
        9: "PKSN_measurement_status",
        10: "Height_of_freshly_fallen_snow_[cm]",
        11: "HSS_measurement_status",
        12: "Snow_species",
        13: "GATS_measurement_status",
        14: "Type_of_snow_cover",
        15: "RPSN_measurement_status"}, inplace=True)
    # data = data.append(csv_data)
    csv_data.to_json(r"/home/dawid/Downloads/meteorological_data.json", orient="records")
    print(csv_data)
    i += 1
    print(f"Processed {i} of {length}")

