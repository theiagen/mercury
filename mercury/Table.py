import pandas as pd
import numpy as np
import re


class Table:
  """This class controls the manipulation of the table
  """
  
  def __init__(self, input_table, table_name, samplenames, skip_county, clearlabs_data, reads_dehosted):
    self.input_table = input_table
    self.table_name = table_name
    self.samplenames = samplenames
    self.skip_county = skip_county
    self.clearlabs_data = clearlabs_data
    self.reads_dehosted = reads_dehosted  

  def get_year_from_date(date):
    r = re.compile('^\d{4}-\d{2}-\d{2}')      
    if pd.isna(date):
      print("Incorrect collection date format; collection date must be in YYYY-MM-DD format. Invalid date was: NaN")
    elif r.match(date) is None:
      print("Incorrect collection date format; collection date must be in YYYY-MM-DD format. Invalid date was: " + str(date))
      return np.nan
    else:
      return date.split("-")[0]
        
  def create_table(self):
    table = pd.read_csv(self.input_table, sep="\t", header=0, dtype={self.table_name: 'str'})
    return table

  def extract_samples(self, table):
    working_table = table[table[self.table_name].isin(self.samplenames.split(","))]
    working_table.columns = working_table.columns.str.lower()
    return working_table
    
  def create_standard_variables(self, table):
    table["year"] = table["collection_date"].apply(lambda x: self.get_year_from_date(x))
    table["host"] = "Human" #(????)
    
  def remove_nas(self, table, required_metadata):
    """This function removes rows with missing values in the required metadata columns and returns the cleaned table and a table of excluded samples

    Args:
        table (DataFrame): Table containing metadata
        required_metadata (List): List of columns that are required to have values
    """
    # replace blank cells with NaNs (blanks are missing values)
    table.replace(r'^\s+$', np.nan, regex=True)
    # remove rows with missing values in the required metadata columns
    excluded_samples = table[table[required_metadata].isna().any(axis=1)]
    # set the index to the sample name
    excluded_samples.set_index("~{table_name}_id".lower(), inplace=True)
    # remove all optional columns so only required columns are shown
    excluded_samples = excluded_samples[excluded_samples.columns.intersection(required_metadata)]
    # remove all NON-NA columns so only columns with NAs remain; Shelly is a wizard and I love her 
    excluded_samples = excluded_samples.loc[:, excluded_samples.isna().any()] 
    # remove all rows that are required with NaNs from table
    table.dropna(subset=required_metadata, axis=0, how='any', inplace=True) 

    return table, excluded_samples


  def process_table(self):
    table = self.create_table()
    table = self.extract_samples(table)
    self.create_standard_variables(table)
    return table