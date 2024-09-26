import pandas as pd
from sqlalchemy import create_engine, text

pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 120)

postgres_user = "postgres"
postgres_password = "sqltrainer"
postgres_host = "localhost"
postgres_port = "5432"
postgres_db = "census_data"

engine = create_engine(
    f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}")

# Task 7: Run Query on the database and show output on streamlit

# 1. What is the total population of each district?
query1 = 'select "District_code","District","Population" from census_2011;'
result_df1 = pd.read_sql_query(query1, con=engine)
# print(result_df1)

# 2. How many literate males and females are there in each district?
query2 = 'select "District_code","District","Literate_Male","Literate_Female","Literate" from census_2011;'
result_df2 = pd.read_sql_query(query2, con=engine)
# print(result_df2)

# 3. What is the percentage of workers (both male and female) in each district?
query3 = ('select "District",round( CAST(float8 ("Workers"/"Population"*100) as numeric), 2) as percentage_of_workers '
          'from census_2011;')
result_df3 = pd.read_sql_query(query3, con=engine)
# print(result_df3)

# 4. How many households have access to LPG or PNG as a cooking fuel in each district?
query4 = 'select "District_code","District","LPG_or_PNG_Households" from census_2011;'
result_df4 = pd.read_sql_query(query4, con=engine)
# print(result_df4)

# 5. What is the religious composition (Hindus, Muslims, Christians, etc.) of each district?
query5 = ('select "District_code","District","Hindus","Muslims","Christians","Sikhs","Buddhists","Jains",'
          '"Others_Religions" as others,"Religion_Not_Stated" from census_2011;')
result_df5 = pd.read_sql_query(query5, con=engine)
# print(result_df5)

# 6. How many households have internet access in each district?
query6 = 'select "District_code","District","Households_with_Internet" from census_2011'
result_df6 = pd.read_sql_query(query6, con=engine)
# print(result_df6)

# 7. What is the educational attainment distribution (below primary, primary, middle, secondary, etc.) in each district?
query7 = ('select "District_code","District","Below_Primary_Education","Primary_Education","Middle_Education",'
          '"Secondary_Education","Higher_Education","Graduate_Education","Other_Education" from census_2011;')
result_df7 = pd.read_sql_query(query7, con=engine)
# print(result_df7)

# 8. How many households have access to various modes of transportation (bicycle, car, radio, television, etc.)
# in each district?
query8 = ('select "District_code","District","Households_with_Scooter_Motorcycle_Moped","Households_with_Bicycle",'
          '"Households_with_Car_Jeep_Van" from census_2011;')
result_df8 = pd.read_sql_query(query8, con=engine)
# print(result_df8)

# 9. What is the condition of occupied census houses (dilapidated, with separate kitchen,
# with bathing facility, with latrine facility, etc.) in each district?
query9 = ('select "District_code","District","Dilapidated_Households",'
          '"Households_with_separate_kitchen_Cooking_inside_house","Having_bathing_facility_Total_Households",'
          '"Latrine_Within_premises" from census_2011;')
result_df9 = pd.read_sql_query(query9, con=engine)
# print(result_df9)

# 10. How is the household size distributed (1 person, 2 persons, 3-5 persons, etc.) in each district?
query10 = ('select "District_code","District","Household_size_1_person_Households",'
           '"Household_size_2_persons_Households","Household_size_1_to_2_persons",'
           '"Household_size_3_persons_Households","Household_size_3_to_5_persons_Households",'
           '"Household_size_4_persons_Households","Household_size_5_persons_Households",'
           '"Household_size_6_8_persons_Households","Household_size_9_persons_and_above_Households" from census_2011;')

result_df10 = pd.read_sql_query(query10, con=engine)
# print(result_df10)

# 11. What is the total number of households in each state?
query11 = 'select "State/UT",SUM("Households") as "Total_Households" from census_2011 group by "State/UT";'
result_df11 = pd.read_sql_query(query11, con=engine)
# print(result_df11)

# 12. How many households have a latrine facility within the premises in each state?
query12 = ('select "State/UT",SUM("Latrine_Within_premises") as '
           '"Households_With_Latrine_Inside" from census_2011  group by "State/UT";')
result_df12 = pd.read_sql_query(query12, con=engine)
# print(result_df12)

# 13. What is the average household size in each state?
query13 = ('select "State/UT",round( CAST(float8 (SUM("Population")/SUM("Households")) as numeric), 2) '
           'as average_household_size from census_2011 group by "State/UT";')
# print(result_df13)

# 14. How many households are owned versus rented in each state?
query14 = ('select "State/UT",SUM("Ownership_Owned_Households") as "owned_homes",SUM("Ownership_Rented_Households") as '
           '"rented_homes" from census_2011 group by "State/UT"')
result_df14 = pd.read_sql_query(query14, con=engine)
# print(result_df14)

# 15. What is the distribution of different types of latrine facilities (pit latrine, flush latrine, etc.) in each
# state?
query15 = ('select "State/UT",SUM("Type_of_latrine_facility_Pit_latrine_Households") as '
           'latrine_facility_Pit_latrine_Households,SUM("Type_of_latrine_facility_Other_latrine_Households") as '
           'latrine_facility_Other_latrine_Households,SUM("latrine_disposed_night_soil_to_pit") as '
           'latrine_disposed_night_soil_to_pit,SUM("latrine_flush_connected_other_household") as '
           'latrine_flush_connected_other_household  from census_2011 group by "State/UT"')
result_df15 = pd.read_sql_query(query15, con=engine)
# print(result_df15)

# 16. How many households have access to drinking water sources near the premises in each state?
query16 = 'select "State/UT",SUM("drinking_water_source_Near_the_premises") from census_2011 group by "State/UT"'
result_df16 = pd.read_sql_query(query16, con=engine)
# print(result_df16)

# 17. What is the average household income distribution in each state based on the power parity categories?
query17 = ('select "State/UT",AVG("Power_Parity_Less_than_Rs_45000") as avg_Power_Parity_Less_than_Rs_45000 ,'
           'AVG("Power_Parity_Rs_45000_90000") as avg_Power_Parity_Rs_45000_90000,AVG("Power_Parity_Rs_90000_150000") '
           'as avg_Power_Parity_Rs_90000_150000,AVG("Power_Parity_Rs_45000_150000") as '
           'avg_Power_Parity_Rs_45000_150000,AVG("Power_Parity_Rs_150000_240000") as '
           'avg_Power_Parity_Rs_150000_240000,AVG("Power_Parity_Rs_240000_330000") as '
           'avg_Power_Parity_Rs_240000_330000,AVG("Power_Parity_Rs_150000_330000") as '
           'avg_Power_Parity_Rs_150000_330000,AVG("Power_Parity_Rs_330000_425000") as '
           'avg_Power_Parity_Rs_330000_425000,AVG("Power_Parity_Rs_425000_545000") as '
           'avg_Power_Parity_Rs_425000_545000,AVG("Power_Parity_Rs_330000_545000") as '
           'avg_Power_Parity_Rs_330000_545000,AVG("Power_Parity_Above_Rs_545000") as '
           'avg_Power_Parity_Above_Rs_545000,'
           'AVG("Total_Power_Parity") as avg_Total_Power_Parity from census_2011 group by "State/UT";')
result_df17 = pd.read_sql_query(query17, con=engine)
# print(result_df17)

# 18. What is the percentage of married couples with different household sizes in each state?
query18 = ('select "State/UT",SUM("Married_couples_1_Households")/SUM("Households")*100 as '
           'percent_1_married_couple_per_Household,SUM("Married_couples_2_Households")/SUM("Households")*100 as '
           'percent_2_married_couple_per_Household,SUM("Married_couples_3_Households")/SUM("Households")*100 as '
           'percent_3_married_couple_per_Household,SUM("Married_couples_3_or_more_Households")/SUM("Households")*100 '
           'as percent_3_or_more_married_couple_per_Household,SUM("Married_couples_4_Households")/SUM('
           '"Households")*100 as percent_4_married_couple_per_Household,SUM("Married_couples_5__Households")/SUM('
           '"Households")*100 as percent_5_married_couple_per_Household,SUM("Married_couples_None_Households")/SUM('
           '"Households")*100 as percent_0_married_couple_per_Household from census_2011 group by "State/UT"')
result_df18 = pd.read_sql_query(query18, con=engine)
# print(result_df18)

# 19. How many households fall below the poverty line in each state based on the power parity categories?
query19 = ('select "State/UT",SUM("Power_Parity_Less_than_Rs_45000") as households_below_Poverty_line from census_2011 '
           'group by "State/UT"')
result_df19 = pd.read_sql_query(query19, con=engine)
# print(result_df18)

# 20 .What is the overall literacy rate (percentage of literate population) in each state?
query20 = ('select "State/UT",round( CAST(float8 ((SUM("Literate")/SUM("Population"))*100) as numeric), '
           '2) as percent_literacy_rate from census_2011 group by "State/UT" order by percent_literacy_rate DESC;')
result_df20 = pd.read_sql_query(query20, con=engine)
print(result_df20)
