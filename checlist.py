# BELOW CODES ARE FOR TESTING ONLY , NO Functionality


import pandas as pd

TELENGANA_DIST = ["Adilabad", "Nizamabad", "Karimnagar", "Medak", "Hyderabad", "Rangareddy", "Mahbubnagar", "Nalgonda",
                  "Warangal", "Khammam"]

pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 120)

census_data = pd.read_csv("census_2011 - census_2011.csv.csv")

# Get the column names
column_names = census_data.columns.tolist()

# Find columns with long names (e.g., longer than 30 characters)
long_columns = [name for name in column_names if len(name) > 55]

# Print the long column names
print("Columns with long names:")
for col in long_columns:
    print(col)


def format_dist_name(name):
    words = name.split()
    formatted = []
    for word in words:
        if word.lower() == "and":
            formatted.append(word.lower())
        else:
            formatted.append(word.capitalize())
    return ' '.join(formatted)


# # GUVI TASK 1
# census_data.rename(columns={"State name": "State/UT", "District name": "District",
#                             "Male_Literate": "Literate_Male",
#                             "Female_Literate": "Literate_Female",
#                             "Rural_Households": "Households_Rural",
#                             "Urban_Households": "Households_Urban",
#                             "Age_Group_0_29": "Young_and_Adult",
#                             "Age_Group_30_49": "Middle_Aged",
#                             "Age_Group_50": "Senior_Citizen",
#                             "Age not stated": "Age_Not_Stated",
#                             }, inplace=True)
#
# # GUVI TASK 2
# census_data["District"] = census_data["District"].apply(format_dist_name)
#
#
# # Program Check
#
# columns_to_check = ["Young_and_Adult", "Middle_Aged", "Senior_Citizen", "Age_Not_Stated"]
#
# # Count the NA values in the specified columns
# na_counts = census_data[columns_to_check].isna().sum().sort_values(ascending=False)
#
# # Convert to DataFrame for better readability
# na_counts_df = na_counts.reset_index()
# na_counts_df.columns = ['Column', 'NA_Count']
#
# print(na_counts_df)
#
#
# # Count of missing education related columns
#
# education_columns = [
#         "Below_Primary_Education",
#         "Primary_Education",
#         "Middle_Education",
#         "Secondary_Education",
#         "Higher_Education",
#         "Graduate_Education",
#         "Other_Education"
#     ]
#
# print(census_data[education_columns].isna().sum())

