import pandas as pd

from pymongo import MongoClient

from sqlalchemy import create_engine, text

import psycopg2

TELENGANA_DIST = ["Adilabad", "Nizamabad", "Karimnagar", "Medak", "Hyderabad", "Rangareddy", "Mahbubnagar", "Nalgonda",
                  "Warangal", "Khammam"]

pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 120)

census_data = pd.read_csv("census_2011 - census_2011.csv.csv")


# Function to format the district names
def format_dist_name(name):
    words = name.split()
    formatted = []
    for word in words:
        if word.lower() == "and":
            formatted.append(word.lower())
        else:
            formatted.append(word.capitalize())
    return ' '.join(formatted)


# Function to fill all missing education related information

def fill_missing_education(df):
    education_columns = [
        "Below_Primary_Education",
        "Primary_Education",
        "Middle_Education",
        "Secondary_Education",
        "Higher_Education",
        "Graduate_Education",
        "Other_Education"
    ]

    for index, row in df.iterrows():
        total_education = row["Total_Education"]
        if pd.notna(total_education):
            filled_sum = sum(row[edu_col] for edu_col in education_columns if pd.notna(row[edu_col]))
            for col in education_columns:
                if pd.isna(row[col]):
                    df.at[index, col] = total_education - filled_sum


# GUVI TASK 1 : Rename columns for clarity
census_data.rename(columns={"District code": "District_code",
                            "State name": "State/UT", "District name": "District",
                            "Male_Literate": "Literate_Male",
                            "Female_Literate": "Literate_Female",
                            "Rural_Households": "Households_Rural",
                            "Urban_Households": "Households_Urban",
                            "Age_Group_0_29": "Young_and_Adult",
                            "Age_Group_30_49": "Middle_Aged",
                            "Age_Group_50": "Senior_Citizen",
                            "Age not stated": "Age_Not_Stated",
                            "Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car":
                                "Households_with_Modern_devices_and_transport",
                            "Condition_of_occupied_census_houses_Dilapidated_Households": "Dilapidated_Households",
                            "Having_latrine_facility_within_the_premises_Total_Households": "Latrine_Within_premises",
                            "Type_of_bathing_facility_Enclosure_without_roof_Households":
                                "bathing_facility_without_roof",
                            "Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households":
                                "latrine_disposed_night_soil_to_pit",
                            "Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households":
                                "latrine_flush_connected_other_household",
                            "Not_having_bathing_facility_within_the_premises_Total_Households":
                                "no_bathing_facility_within_premises",
                            "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households":
                                "no_latrine_within_household_open_source_alternative",
                            "Main_source_of_drinking_water_Un_covered_well_Households":
                                "drinking_water_uncovered_well_source",
                            "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households":
                                "drinking_water_mechanical_well_source",
                            "Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households":
                                "drinking_water_natural_water_source",
                            "Location_of_drinking_water_source_Near_the_premises_Households":
                                "drinking_water_source_Near_the_premises",
                            "Location_of_drinking_water_source_Within_the_premises_Households":
                                "drinking_water_source_Within_the_premises",
                            "Main_source_of_drinking_water_Tubewell_Borehole_Households":
                                "drinking_water_Borehole_well_source"
                            }, inplace=True)

# GUVI TASK 2: Format the district names
census_data["District"] = census_data["District"].apply(format_dist_name)

# GUVI TASK 3: Update state information for specific districts

census_data.loc[census_data["District"].isin(TELENGANA_DIST), "State/UT"] = "Telangana"

census_data.loc[census_data["District"].isin(["Leh(ladakh)", "Kargil"]), "State/UT"] = "Ladakh"

# GUVI TASK 4: Handle missing values
# Uncomment to check for missing values percentage
# cols_missing_percentage = census_data.isna().mean() * 100
# print(cols_missing_percentage)

# fill population missing data
census_data["Female"] = census_data["Female"].fillna(census_data["Population"] - census_data["Male"])

census_data["Male"] = census_data["Male"].fillna(census_data["Population"] - census_data["Female"])

# Update Population where "Male" is missing using the sum of (Male_Workers, Female_Workers, Non_Workers)
census_data.loc[census_data["Male"].isna(), "Population"] = (
        census_data["Male_Workers"] + census_data["Female_Workers"] + census_data["Non_Workers"]
)
census_data["Male"] = census_data["Male"].fillna(census_data["Population"] - census_data["Female"])

census_data["Population"] = census_data["Population"].fillna(census_data["Male"] + census_data["Female"])

# Update Literacy data

census_data["Literate"] = census_data["Literate"].fillna(census_data["Literate_Male"] + census_data["Literate_Female"])
census_data["Literate"] = census_data["Literate"].fillna(census_data["Literate_Education"])

census_data["Literate_Female"] = census_data["Literate_Female"].fillna(census_data["Literate"] -
                                                                       census_data["Literate_Male"])
census_data["Literate_Male"] = census_data["Literate_Male"].fillna(census_data["Literate"] -
                                                                   census_data["Literate_Female"])

# Update Households

census_data["Hoseholds"] = census_data["Households"].fillna(census_data["Households_Rural"] +
                                                            census_data["Households_Urban"])
census_data["Households_Urban"] = census_data["Households_Urban"].fillna(census_data["Households"] -
                                                                         census_data["Households_Rural"])

census_data["Households_Rural"] = census_data["Households_Rural"].fillna(census_data["Households"] -
                                                                         census_data["Households_Urban"])

census_data["Ownership_Owned_Households"] = (census_data["Ownership_Owned_Households"].fillna(census_data["Households"])
                                             - census_data["Ownership_Rented_Households"])
census_data["Ownership_Rented_Households"] = (
        census_data["Ownership_Rented_Households"].fillna(census_data["Households"]) - census_data["Ownership_Owned_Households"])

# Update SC, ST, Workers --> Total = Male + Female

census_data["SC"] = census_data["SC"].fillna(census_data["Male_SC"] +
                                             census_data["Female_SC"])
census_data["ST"] = census_data["ST"].fillna(census_data["Male_ST"] +
                                             census_data["Female_ST"])
census_data["Workers"] = census_data["Workers"].fillna(census_data["Male_Workers"] +
                                                       census_data["Female_Workers"])

# Update the Age based data , Population - Sum of all other age categories

census_data["Middle_Aged"] = census_data["Middle_Aged"].fillna(census_data["Population"] -
                                                               (census_data["Age_Not_Stated"] +
                                                                census_data["Young_and_Adult"] +
                                                                census_data["Senior_Citizen"]))

census_data["Senior_Citizen"] = census_data["Senior_Citizen"].fillna(census_data["Population"] -
                                                                     (census_data["Age_Not_Stated"] +
                                                                      census_data["Young_and_Adult"] +
                                                                      census_data["Middle_Aged"]))

census_data["Young_and_Adult"] = census_data["Young_and_Adult"].fillna(census_data["Population"] -
                                                                       (census_data["Age_Not_Stated"] +
                                                                        census_data["Senior_Citizen"] +
                                                                        census_data["Middle_Aged"]))

census_data["Age_Not_Stated"] = census_data["Age_Not_Stated"].fillna(census_data["Population"] -
                                                                     (census_data["Young_and_Adult"] +
                                                                      census_data["Senior_Citizen"] +
                                                                      census_data["Middle_Aged"]))

# Update the Education based data , Total Education - Sum of other relevant education categories

fill_missing_education(census_data)

# GUVI TASK 5 : Import Data to MongoDB

client = MongoClient("mongodb://localhost:27017/")
db = client["census_data"]
collection = db["census_2011"]

data_dict = census_data.to_dict(orient="records")
collection.insert_many(data_dict)

# GUVI TASK 6 : Import Data to RDBMS (Postgres)

postgres_user = "postgres"
postgres_password = "sqltrainer"
postgres_host = "localhost"
postgres_port = "5432"
postgres_db = "census_data"

engine = create_engine(
    f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}")

mongo_census_data = list(collection.find())

if mongo_census_data:
    # Convert to DataFrame
    mongo_data_df = pd.DataFrame(mongo_census_data)

    mongo_data_df.drop(columns=["_id"], inplace=True, errors="ignore")

    mongo_data_df.set_index("District_code", inplace=True)

    mongo_data_df.to_sql("census_2011", con=engine, if_exists="replace", index=True)

print("Data uploaded to PostgreSQL successfully.")

