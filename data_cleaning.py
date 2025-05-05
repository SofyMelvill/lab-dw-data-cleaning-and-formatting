import pandas as pd
url = 'https://raw.githubusercontent.com/data-bootcamp-v4/data/main/file1.csv'
insur_comp_df = pd.read_csv(url)

# format column names
def formating_column_names(insur_comp_df):
    insur_comp_df.columns = insur_comp_df.columns.str.strip().str.lower().str.replace(' ', '_')
    return insur_comp_df

# renaming the columns , in this case st for state
def rename_columns(insur_comp_df):
    insur_comp_df = insur_comp_df.rename(columns={'st': 'state'})
    return insur_comp_df


# correct bad written values (states, education, vehicle class, etc.)
def correct_values(insur_comp_df):
    insur_comp_df["state"] = insur_comp_df["state"].replace({"Cali" : "California","CALI" : "California", "WA" : "Whashington", "Washington" : "Whashington", "AZ" : "Arizona"})
    insur_comp_df["education"] = insur_comp_df["education"].replace({"Bachelors": "Bachelor"})
    insur_comp_df["vehicle_class"] = insur_comp_df["vehicle_class"].replace({"Luxury SUV" : "Luxury", "Luxury Car" : "Luxury","Sports Car" : "Luxury"})
    return insur_comp_df


# clean gender column
def clean_category(insur_comp_df, column, replacement_map):
    insur_comp_df[column] = (insur_comp_df[column].astype(str).str.strip().str.title().replace(replacement_map))
    return insur_comp_df


# clean percentages 
def clean_percentages (insur_comp_df, column):
    insur_comp_df[column] = insur_comp_df[column].astype(str).str.rstrip("%").astype(float)
    return insur_comp_df

# convert columns to numeric
def convert_to_numeric(insur_comp_df, column):
    insur_comp_df[column] = pd.to_numeric(insur_comp_df[column], errors="coerce")
    return insur_comp_df

# fillna with median
def fillna_median(insur_comp_df, column):
    median_ = insur_comp_df[column].median()
    insur_comp_df[column] = insur_comp_df[column].fillna(median_)
    return insur_comp_df

# fillna with mode
def fillna_mode(insur_comp_df, column):
    if not isinstance(insur_comp_df, pd.DataFrame):
        raise TypeError ("This is a series and we expected a DataFrame")

    mode_ = insur_comp_df[column].mode()[0]
    insur_comp_df[column] = insur_comp_df[column].fillna(mode_)
    return insur_comp_df

# remove all null rows
def remove_empty_rows(insur_comp_df):
    return insur_comp_df.dropna(how="all")

# verify duplicates - reminding that I choose not to remove duplicates
def check_duplicates(insur_comp_df, column):
    duplicates = insur_comp_df[insur_comp_df[column].duplicated(keep=False)]
    if duplicates.empty:
        print(f"No duplicates found in the column '{column}'.")
    else:
        print(f"Duplicates found in columns '{column}':\n", duplicates[[column]])
    return insur_comp_df

# Main function

def main(filepath):
    insur_comp_df = pd.read_csv(filepath)

    insur_comp_df = formating_column_names(insur_comp_df)
    
    print("Available columns:", insur_comp_df.columns.tolist())

    insur_comp_df = rename_columns(insur_comp_df)
    insur_comp_df = correct_values(insur_comp_df)
    insur_comp_df = remove_empty_rows(insur_comp_df)

    insur_comp_df = clean_percentages (insur_comp_df, "customer_lifetime_value")
    insur_comp_df = convert_to_numeric(insur_comp_df, "number_of_open_complaints")

    insur_comp_df = fillna_median(insur_comp_df, "customer_lifetime_value")
    insur_comp_df = fillna_mode(insur_comp_df, "gender")

    insur_comp_df = clean_category(insur_comp_df, "gender", {"Male" : "M","Female" : "F"})
    insur_comp_df = clean_category(insur_comp_df, "education", {})

    insur_comp_df = check_duplicates(insur_comp_df, "customer") # doesn't remove, just checks

    insur_comp_df.to_csv("cleaned_insurance_data.csv", index = False)
    print("The data is cleaned and saved  as 'cleaned_data.csv'")

    return insur_comp_df