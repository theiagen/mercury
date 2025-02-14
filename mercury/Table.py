import pandas as pd
import numpy as np
import subprocess
import re
import sys


class Table:
  """This class controls the manipulation of the table
  """
  
  def __init__(self, logger, organism, input_table, table_name, samplenames, skip_county, skip_ncbi, 
               usa_territory, metadata_list, vadr_alert_limit, number_n_threshold, assembly_fasta_column_name, 
               output_prefix, gcp_bucket_uri, single_end, read1_column_name, assembly_mean_coverage_column_name, 
               authors, bioproject_accession, continent, country, host_disease, isolation_source, library_selection, 
               library_source, library_strategy, purpose_of_sequencing, state, submitting_lab, submitting_lab_address, 
               amplicon_primer_scheme, amplicon_size, instrument_model, library_layout, seq_platform, 
               gisaid_submitter, submitter_email, read2_column_name=""):
    self.logger = logger
    self.logger.debug("TABLE:Initializing Table class")
    
    self.organism = organism
    self.input_table = input_table
    self.table_name = table_name
    self.samplenames = samplenames
    self.skip_county = skip_county
    self.skip_ncbi = skip_ncbi
    self.usa_territory = usa_territory
    self.metadata_list = metadata_list
    
    self.vadr_alert_limit = vadr_alert_limit
    self.number_n_threshold = number_n_threshold
    self.assembly_fasta_column_name = assembly_fasta_column_name
    self.read1_column_name = read1_column_name
    self.read2_column_name = read2_column_name
    self.assembly_mean_coverage_column_name = assembly_mean_coverage_column_name
  
    self.output_prefix = output_prefix
    self.exclusion_table_name = self.output_prefix + "_excluded_samples.tsv"

    self.gcp_bucket_uri = gcp_bucket_uri
    self.single_end = single_end
    self.authors = authors
    self.bioproject_accession = bioproject_accession
    self.continent = continent
    self.country = country
    self.host_disease = host_disease
    self.isolation_source = isolation_source
    self.library_selection = library_selection
    self.library_source = library_source
    self.library_strategy = library_strategy
    self.purpose_of_sequencing = purpose_of_sequencing
    self.state = state
    self.submitting_lab = submitting_lab
    self.submitting_lab_address = submitting_lab_address
    self.amplicon_primer_scheme = amplicon_primer_scheme
    self.amplicon_size = amplicon_size
    self.instrument_model = instrument_model
    self.library_layout = library_layout
    self.seq_platform = seq_platform
    self.gisaid_submitter = gisaid_submitter
    self.submitter_email = submitter_email

    # transform the input table into a pandas dataframe
    self.logger.debug(f"TABLE:Loading input table {self.input_table}")
    self.table = pd.read_csv(self.input_table, sep="\t", header=0, dtype={self.table_name: 'str'})

  def get_year_from_date(self, date):
    """This function extracts the year from a date in ISO 8601 format

    Args:
      date (String): The date in ISO 8601 format (YYYY-MM-DD)

    Returns:
      Int: The year from the date, or np.nan if the date is not in the correct format
    """
    r = re.compile('^\d{4}-\d{2}-\d{2}')      
    if pd.isna(date) or r.match(date) is None:
      self.logger.debug("TABLE:Incorrect collection date format; collection date must be in YYYY-MM-DD format. Invalid date was: " + str(date))
      return np.nan
    else:
      return date.split("-")[0]
           
  def extract_samples(self):
    """This function pulls out the rows that belong to each sample in the samplenames list. It also converts the column names to lowercase.
    
    Returns:
      DataFrame: The reduced table with lowercase headers
    """
    self.logger.debug("TABLE:Extracting samples from table")
    working_table = self.table[self.table[self.table_name].isin(self.samplenames)]
    working_table.columns = working_table.columns.str.lower()
    self.table = working_table
    
  def create_standard_variables(self):
    """This function creates standard variables in the table
    """
    self.logger.debug("TABLE:Creating standard variables like date and host")
    self.table["organism"] = self.organism
    # Overwrite preexisting inputs if these values do not evaluate to False
    if self.authors:
      self.table["authors"] = self.authors
      self.logger.debug(f"TABLE:Authors were provided, overwriting authors column with {self.authors}")
    if self.bioproject_accession:
      self.table["bioproject_accession"] = self.bioproject_accession
      self.logger.debug(f"TABLE:BioProject accession was provided, overwriting BioProject accession column with {self.bioproject_accession}")
    if self.continent:
      self.table["continent"] = self.continent
      self.logger.debug(f"TABLE:Continent was provided, overwriting continent column with {self.continent}")
    if self.country:
      self.table["country"] = self.country
      self.logger.debug(f"TABLE:Country was provided, overwriting country column with {self.country}")
    if self.host_disease:
      self.table["host_disease"] = self.host_disease
      self.logger.debug(f"TABLE:Host disease was provided, overwriting host_disease column with {self.host_disease}")
    if self.isolation_source:
      self.table["isolation_source"] = self.isolation_source
      self.logger.debug(f"TABLE:Isolation source was provided, overwriting isolation_source column with {self.isolation_source}")
    if self.library_selection:
      self.table["library_selection"] = self.library_selection
      self.logger.debug(f"TABLE:Library selection was provided, overwriting library_selection column with {self.library_selection}")
    if self.library_source:
      self.table["library_source"] = self.library_source
      self.logger.debug(f"TABLE:Library source was provided, overwriting library_source column with {self.library_source}")
    if self.library_strategy:
      self.table["library_strategy"] = self.library_strategy
      self.logger.debug(f"TABLE:Library strategy was provided, overwriting library_strategy column with {self.library_strategy}")
    if self.purpose_of_sequencing:
      self.table["purpose_of_sequencing"] = self.purpose_of_sequencing
      self.logger.debug(f"TABLE:Purpose of sequencing was provided, overwriting purpose_of_sequencing column with {self.purpose_of_sequencing}")
    if self.state:
      self.table["state"] = self.state
      self.logger.debug(f"TABLE:State was provided, overwriting state column with {self.state}")
    if self.submitting_lab:
      self.table["submitting_lab"] = self.submitting_lab
      self.logger.debug(f"TABLE:Submitting lab was provided, overwriting submitting_lab column with {self.submitting_lab}")
    if self.submitting_lab_address:
      self.table["submitting_lab_address"] = self.submitting_lab_address
      self.logger.debug(f"TABLE:Submitting lab address was provided, overwriting submitting_lab_address column with {self.submitting_lab_address}")
    if self.amplicon_primer_scheme:
      self.table["amplicon_primer_scheme"] = self.amplicon_primer_scheme
      self.logger.debug(f"TABLE:Amplicon primer scheme was provided, overwriting amplicon_primer_scheme column with {self.amplicon_primer_scheme}")
    if self.amplicon_size:
      self.table["amplicon_size"] = self.amplicon_size
      self.logger.debug(f"TABLE:Amplicon size was provided, overwriting amplicon_size column with {self.amplicon_size}")
    if self.instrument_model:
      self.table["instrument_model"] = self.instrument_model
      self.logger.debug(f"TABLE:Instrument model was provided, overwriting instrument_model column with {self.instrument_model}")
    if self.library_layout:
      self.table["library_layout"] = self.library_layout
      self.logger.debug(f"TABLE:Library layout was provided, overwriting library_layout column with {self.library_layout}")
    if self.seq_platform:
      self.table["seq_platform"] = self.seq_platform
      self.logger.debug(f"TABLE:Sequencing platform was provided, overwriting seq_platform column with {self.seq_platform}")
    if self.gisaid_submitter:
      self.table["gisaid_submitter"] = self.gisaid_submitter
      self.logger.debug(f"TABLE:GISAID submitter was provided, overwriting gisaid_submitter column with {self.gisaid_submitter}")
    if self.submitter_email:
      self.table["submitter_email"] = self.submitter_email
      self.logger.debug(f"TABLE:Submitter email was provided, overwriting submitter_email column with {self.submitter_email}")

    self.table["year"] = self.table["collection_date"].apply(lambda x: self.get_year_from_date(x))
    self.table["host"] = "Human" #(????)
    if self.skip_ncbi:
      self.logger.debug("TABLE:Skipping creating NCBI-specific variables")
    else:
      self.logger.debug("TABLE:Creating NCBI-specific variables")
      self.table["host_sci_name"] = "Homo sapiens"
      self.table["filetype"] = "fastq"
      
      if self.organism != "flu":
        self.table["isolate"] = (self.table["organism"] + "/" + self.table["host"] + "/" + self.table["country"] + "/" + self.table["submission_id"] + "/" + self.table["year"])
      
      self.table["biosample_accession"] = "{populate_with_BioSample_accession}"
      self.table["design_description"] = "Whole genome sequencing of " + self.table["organism"] 
    
    if self.organism == "sars-cov-2":
      self.table["gisaid_organism"] = "hCoV-19"
    elif self.organism == "mpox":
      self.table["gisaid_organism"] = "mpx/A"

    if self.organism != "flu":
      self.logger.debug("TABLE: populating gisaid_virus_name")
      if self.usa_territory:
        # if usa territory, use "state" (e.g., Puerto Rico) instead of country (USA)
        self.table["gisaid_virus_name"] = (self.table["gisaid_organism"] + "/" + self.table["state"] + "/" + self.table["submission_id"] + "/" + self.table["year"])
      else: 
        self.table["gisaid_virus_name"] = (self.table["gisaid_organism"] + "/" + self.table["country"] + "/" + self.table["submission_id"] + "/" + self.table["year"])

      
  def remove_nas(self):
    """This function removes rows with missing values in the required metadata columns and writes them to a file
    """
    # replace blank cells with NaNs (blanks are missing values)
    self.table.replace(r'^\s+$', np.nan, regex=True)
    # remove rows with missing values in the required metadata columns
    excluded_samples = self.table[self.table[self.required_metadata].isna().any(axis=1)]
    # set the index to the sample name
    excluded_samples.set_index(self.table_name.lower(), inplace=True)
    # remove all optional columns so only required columns are shown
    excluded_samples = excluded_samples[excluded_samples.columns.intersection(self.required_metadata)]
    # remove all NON-NA columns so only columns with NAs remain; Shelly is a wizard and I love her 
    excluded_samples = excluded_samples.loc[:, excluded_samples.isna().any()] 
    # remove all rows that are required with NaNs from table
    self.table.dropna(subset=self.required_metadata, axis=0, how='any', inplace=True) 

    with open(self.exclusion_table_name, "a") as exclusions:
      exclusions.write("\nSamples excluded for missing required metadata (will have empty values in indicated columns):\n")
    excluded_samples.to_csv(self.exclusion_table_name, mode='a', sep='\t')
    
  def perform_quality_check(self):
    """This function removes samples based on the number of VADR alerts and the number of Ns (for "sars-cov-2" only) and writes them to a file
    """
    quality_exclusion = pd.DataFrame()
    for index, row in self.table.iterrows():
      if ("VADR skipped due to poor assembly") in str(row["vadr_num_alerts"]):
        notification = "VADR skipped due to poor assembly"
        quality_exclusion = pd.concat([quality_exclusion, pd.Series({"sample_name": row[self.table_name.lower()], "message": notification}).to_frame().T], ignore_index=True)
      elif int(row["vadr_num_alerts"]) > self.vadr_alert_limit:
        notification = "VADR number alerts too high: " + str(row["vadr_num_alerts"]) + " greater than limit of " + str(self.vadr_alert_limit)
        quality_exclusion = pd.concat([quality_exclusion, pd.Series({"sample_name": row[self.table_name.lower()], "message": notification}).to_frame().T], ignore_index=True)
      elif int(row["number_n"]) > self.number_n_threshold:
        notification="Number of Ns was too high: " + str(row["number_n"]) + " greater than limit of " + str(self.number_n_threshold)
        quality_exclusion = pd.concat([quality_exclusion, pd.Series({"sample_name": row[self.table_name.lower()], "message": notification}).to_frame().T], ignore_index=True)
      if pd.isna(row["year"]):
        notification="The collection date format was incorrect"
        quality_exclusion = pd.concat([quality_exclusion, pd.Series({"sample_name": row[self.table_name.lower()], "message": notification}).to_frame().T], ignore_index=True)

    with open(self.exclusion_table_name, "w") as exclusions:
      exclusions.write("Samples excluded for quality thresholds:\n")
    quality_exclusion.to_csv(self.exclusion_table_name, mode='a', sep='\t', index=False)
      
    self.table.drop(self.table.index[self.table["vadr_num_alerts"].astype(str).str.contains("VADR skipped due to poor assembly")], inplace=True)
    self.table.drop(self.table.index[self.table["vadr_num_alerts"].astype(int) > self.vadr_alert_limit], inplace=True)
    self.table.drop(self.table.index[self.table["number_n"].astype(int) > self.number_n_threshold], inplace=True)
    self.table.drop(self.table.index[self.table["year"].isna()], inplace=True)

  def split_metadata(self):
    self.logger.debug("TABLE:Splitting metadata list into separate lists")
    
    temp_required_metadata = self.metadata_list[0]
    temp_optional_metadata = self.metadata_list[1]
    if self.skip_ncbi:
      self.logger.debug("TABLE:Skipping NCBI submission, removing NCBI-specific metadata requirements")
      self.gisaid_required, self.gisaid_optional = temp_required_metadata[0], temp_optional_metadata[0]
    else:
      self.logger.debug("TABLE:NCBI submission not skipped, keeping NCBI-specific metadata requirements")
      if self.organism == "sars-cov-2":
        self.biosample_required, self.sra_required, self.genbank_required, self.gisaid_required = temp_required_metadata[0], temp_required_metadata[1], temp_required_metadata[2], temp_required_metadata[3]
        self.biosample_optional, self.sra_optional, self.genbank_optional, self.gisaid_optional = temp_optional_metadata[0], temp_optional_metadata[1], temp_optional_metadata[2], temp_optional_metadata[3]
        
      elif self.organism == "flu":
        self.biosample_required, self.sra_required = temp_required_metadata[0], temp_required_metadata[1]
        self.biosample_optional, self.sra_optional = temp_optional_metadata[0], temp_optional_metadata[1]
      
      elif self.organism == "mpox":
        self.biosample_required, self.sra_required, self.bankit_required, self.gisaid_required = temp_required_metadata[0], temp_required_metadata[1], temp_required_metadata[2], temp_required_metadata[3]
        self.biosample_optional, self.sra_optional, self.bankit_optional, self.gisaid_required = temp_optional_metadata[0], temp_optional_metadata[1], temp_optional_metadata[2], temp_optional_metadata[3]

    self.required_metadata = [item for group in temp_required_metadata for item in group]
    if self.skip_ncbi:
      self.required_metadata = self.required_metadata + [self.assembly_fasta_column_name]
    else:
      self.required_metadata = self.required_metadata + [self.assembly_fasta_column_name, self.read1_column_name]
      if not self.single_end:
        self.required_metadata = self.required_metadata + [self.read2_column_name]
    self.optional_metadata = [item for group in temp_optional_metadata for item in group]
  
    self.logger.debug("TABLE:Metadata split!")

  def make_biosample_csv(self):
    self.logger.debug("TABLE:Creating BioSample metadata file")
    biosample_metadata = self.table[self.biosample_required].copy()
    for column in self.biosample_optional:
      if column in self.table.columns:
        biosample_metadata[column] = self.table[column]
      else:
        biosample_metadata[column] = ""
    
    # if either "isolate" or "strain" columns do not exist in input terra table, then set a boolean variable "user_supplied_isolate_or_strain" to False; otherwise set to True
    if "isolate" not in self.table.columns and "strain" not in self.table.columns:
      user_supplied_isolate_or_strain = False
    else:
      user_supplied_isolate_or_strain = True

    biosample_metadata.rename(columns={"submission_id" : "sample_name"}, inplace=True)
    
    if self.organism == "mpox" or self.organism == "sars-cov-2":
      biosample_metadata["geo_loc_name"] = biosample_metadata["country"] + ": " + biosample_metadata["state"]
      biosample_metadata.drop(["country", "state"], axis=1, inplace=True)

      biosample_metadata.rename(columns={"collecting_lab" : "collected_by", "host_sci_name" : "host", "patient_gender" : "host_sex", "patient_age" : "host_age"}, inplace=True)      
      if self.organism == "sars-cov-2":
        biosample_metadata.rename(columns={"treatment" : "antiviral_treatment_agent"}, inplace=True)
    # Flu only: when user does not supply isolate or strain metadata columns, create "isolate" column using the syntax below
    elif self.organism == "flu" and user_supplied_isolate_or_strain == False :
      # type/state/submission_id/year (subtype)
      # strip off "Type_" from beginning of Type, e.g. "Type_A" -> "A"
      self.logger.debug("DEBUG:User did not supply isolate or strain metadata columns, creating isolate column for Flu samples now...")
      print(biosample_metadata["abricate_flu_type"])
      print(biosample_metadata["state"])
      print(biosample_metadata["sample_name"])
      print(biosample_metadata["abricate_flu_subtype"])
      biosample_metadata["isolate"] = (biosample_metadata["abricate_flu_type"].str.replace("Type_","") + "/" + biosample_metadata["state"] + "/" + biosample_metadata["sample_name"] + "/" + biosample_metadata["year"] + " (" + biosample_metadata["abricate_flu_subtype"] + ")")
      print(biosample_metadata["isolate"])
      # Remove 4 extra columns from the output table prior to creating TSV file (these are simply used to create the isolate column)
      biosample_metadata.drop(["abricate_flu_type", "abricate_flu_subtype", "year", "state"], axis=1, inplace=True)

    biosample_metadata.to_csv(self.output_prefix + "_biosample_metadata.tsv", sep='\t', index=False)
    self.logger.debug("TABLE:BioSample metadata file created")

  def make_sra_csv(self):
    self.logger.debug("TABLE:Creating SRA metadata file")
    sra_metadata = self.table[self.sra_required].copy()
    for column in self.sra_optional:
      if column in self.table.columns:
        sra_metadata[column] = self.table[column]
      else:
        sra_metadata[column] = ""
        
    sra_metadata.rename(columns={"submission_id" : "sample_name", "library_id" : "library_ID"}, inplace=True)
  
    if self.organism != "flu":
      # these columns are named differently in the mercury metadata preparation spreadsheets 
      sra_metadata.rename(columns={"amplicon_primer_scheme" : "amplicon_PCR_primer_scheme", "submitter_email" : "sequence_submitter_contact_email", "assembly_method" : "raw_sequence_data_processing_method", "seq_platform" : "platform"}, inplace=True)
      sra_metadata["title"] = "Genomic sequencing of " + sra_metadata["organism"] + ": " + sra_metadata["isolation_source"]
      sra_metadata.drop(["organism", "isolation_source"], axis=1, inplace=True)

    sra_metadata["filename"] = sra_metadata["sample_name"] + "_R1.fastq.gz"
    read_tuples = list(zip(self.table[self.read1_column_name], sra_metadata["filename"]))
    if (self.read2_column_name in self.table.columns) and (self.single_end == False):
      sra_metadata["filename2"] = sra_metadata["sample_name"] + "_R2.fastq.gz"
      read_tuples = read_tuples + list(zip(self.table[self.read2_column_name], sra_metadata["filename2"]))
    elif (self.read2_column_name not in self.table.columns and self.single_end == False):
      self.logger.error("TABLE:Error: Paired-end data was indicated but no read2 column was found in the table")
      sys.exit(1)    

    sra_metadata.to_csv(self.output_prefix + "_sra_metadata.tsv", sep='\t', index=False)
    
    self.logger.info("TABLE:Copying over SRA files to the indicated GCP bucket ({})".format(self.gcp_bucket_uri))
    for oldname, newname in read_tuples:
      check_if_transferred_command = "gcloud storage ls " + self.gcp_bucket_uri + "/" + newname
      self.logger.debug("TABLE:Running command: " + check_if_transferred_command)
      try:
        subprocess.run(check_if_transferred_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.logger.warning("TABLE:Warning: A file with an identical name was found in the destination Google bucket; data transfer will be skipped.")
      except:
        self.logger.debug("TABLE:The data did not appear in the bucket; now attempting to transfer the data")
        
        transfer_command = "gcloud storage cp " + oldname + " " + self.gcp_bucket_uri + "/" + newname
        self.logger.debug("TABLE:Running command: " + transfer_command)
        try:
          subprocess.run(transfer_command, shell=True, check=True)
        except:
          self.logger.error("TABLE:Error: non-zero exit code when copying files to GCP bucket ({})".format(self.gcp_bucket_uri))
          sys.exit(1)
    
    self.logger.info("TABLE:Files copied to the indicated GCP bucket ({})".format(self.gcp_bucket_uri))
    self.logger.debug("TABLE:SRA metadata file created and data transferred")
    
  def make_genbank_csv(self):
    self.logger.debug("TABLE:Creating GenBank metadata file")
    genbank_metadata = self.table[self.genbank_required].copy()
    
    update_country = False
    for column in self.genbank_optional:
      if column in self.table.columns:
        genbank_metadata[column] = self.table[column]
        if column == "state":
          update_country = True
      else:
        genbank_metadata[column] = ""
    
    genbank_metadata.rename(columns={"submission_id" : "Sequence_ID", "host_sci_name" : "host", "collection_date" : "collection-date", "isolation_source" : "isolation-source", "biosample_accession" : "BioSample", "bioproject_accession" : "BioProject", "country" : "geo_loc_name"}, inplace=True)
  
    if update_country:
      genbank_metadata["geo_loc_name"] = genbank_metadata["geo_loc_name"] + ": " + genbank_metadata["state"]
      
    # remove state column from genbank
    genbank_metadata.drop("state", axis=1, inplace=True)
    
    genbank_metadata.to_csv(self.output_prefix + "_genbank_metadata.tsv", sep='\t', index=False)
    self.logger.debug("TABLE:GenBank metadata file created")
    
    
    self.logger.debug("TABLE:Now renaming the header of every fasta file to the preferred format")
    genbank_metadata["new_filenames"] = genbank_metadata["Sequence_ID"] + "_genbank_untrimmed.fasta"
    assembly_tuples = list(zip(self.table[self.assembly_fasta_column_name], genbank_metadata["new_filenames"], genbank_metadata["Sequence_ID"]))
    
    for oldname, newname, sequence_id in assembly_tuples:
      assembly_rename_command = "gcloud storage cp " + oldname + " ./" + newname
      self.logger.debug("TABLE:Running command: " + assembly_rename_command)
      try:
        subprocess.run(assembly_rename_command, shell=True, check=True)
      except:
        self.logger.error("TABLE:Error: non-zero exit code when copying files to working directory")
        sys.exit(1)
      
      sed_command = "sed -i '1s|.*|>" + sequence_id + "|' " + newname
      self.logger.debug("TABLE:Running command: " + sed_command)
      try:
        subprocess.run(sed_command, shell=True, check=True)
      except:
        self.logger.error("TABLE:Error: non-zero exit code when rewriting assembly header")
        sys.exit(1)
        
    self.logger.debug("TABLE:Concatenating GenBank  fasta files")
    cat_command = "cat *_genbank_untrimmed.fasta > " + self.output_prefix + "_genbank_untrimmed_combined.fasta"
    try:
      subprocess.run(cat_command, shell=True, check=True)
    except:
      self.logger.error("TABLE:Error: non-zero exit code when concatenating fasta files")
      sys.exit(1)
    
    self.logger.debug("TABLE:GenBank metadata preparation complete")
    
  def make_bankit_src(self):
    self.logger.debug("TABLE:Creating BankIt metadata file")
    bankit_metadata = self.table[self.bankit_required].copy()
    for column in self.bankit_optional:
      if column in self.table.columns:
        bankit_metadata[column] = self.table[column]
      else:
        bankit_metadata[column] = ""
    bankit_metadata.rename(columns={"submission_id" : "Sequence_ID", "isolate" : "Isolate", "collection_date" : "Collection_date", "country" : "Country", "host" : "Host", "isolation_source" : "Isolation_source"}, inplace=True)

    self.logger.debug("TABLE:Writing BankIt metadata out to a file")
    bankit_metadata.to_csv(self.output_prefix + ".src", sep='\t', index=False)

    self.logger.debug("TABLE:Now renaming the header of every fasta file to the preferred format")
    
    bankit_metadata["new_filenames"] = bankit_metadata["Sequence_ID"] + "_bankit.fasta"
    assembly_tuples = list(zip(self.table[self.assembly_fasta_column_name], bankit_metadata["new_filenames"], bankit_metadata["Sequence_ID"]))
    
    for oldname, newname, sequence_id in assembly_tuples:
      assembly_rename_command = "gcloud storage cp " + oldname + " ./" + newname
      self.logger.debug("TABLE:Running command: " + assembly_rename_command)
      try:
        subprocess.run(assembly_rename_command, shell=True, check=True)
      except:
        self.logger.error("TABLE:Error: non-zero exit code when copying files to working directory")
        sys.exit(1)
      
      sed_command = "sed -i '1s|.*|>" + sequence_id + "|' " + newname
      self.logger.debug("TABLE:Running command: " + sed_command)
      try:
        subprocess.run(sed_command, shell=True, check=True)
      except:
        self.logger.error("TABLE:Error: non-zero exit code when rewriting assembly header")
        sys.exit(1)
    
    self.logger.debug("TABLE:Concatenating BankIt fasta files")
    cat_command = "cat *_bankit.fasta > " + self.output_prefix + "_bankit_combined.fasta"
    try:
      subprocess.run(cat_command, shell=True, check=True)
    except:
      self.logger.error("TABLE:Error: non-zero exit code when concatenating fasta files")
      sys.exit(1)
      
    self.logger.debug("TABLE:BankIt metadata preparation complete")    
 
  def make_gisaid_csv(self):
    self.logger.debug("TABLE:Creating GISAID metadata file")
    gisaid_metadata = self.table[self.gisaid_required].copy()
    
    for column in self.gisaid_optional:
      if column in self.table.columns:
        self.logger.debug("TABLE:Adding column " + column + " to GISAID metadata")
        gisaid_metadata[column] = self.table[column]
      else:
        gisaid_metadata[column] = ""
    
    if self.usa_territory:
      gisaid_metadata["org_location"] = (gisaid_metadata["continent"] + " / " + gisaid_metadata["state"]) 
    else:
      gisaid_metadata["org_location"] = (gisaid_metadata["continent"] + " / " + gisaid_metadata["country"] + " / " + gisaid_metadata["state"]) 
    
    if self.skip_county:
      self.logger.debug("TABLE:Not adding county information to `org_location`")
    else:
      self.logger.debug("TABLE:Adding county information to `org_location`")
      gisaid_metadata["county"] = gisaid_metadata["county"].fillna("")
      gisaid_metadata["org_location"] = gisaid_metadata.apply(lambda x: x["org_location"] + " / " + x["county"] if len(x["county"]) > 0 else x["org_location"], axis=1)

    
    if self.organism == "sars-cov-2":     
      # add additional sc2-specific columns & any empty ones GISAID wants
      gisaid_metadata["covv_type"] = "betacoronavirus"
      gisaid_metadata["covv_passage"] = "original"
      gisaid_metadata["covv_subm_sample_id"] = ""
      gisaid_metadata["covv_provider_sample_id"] = ""
      gisaid_metadata["covv_add_location"] = ""
      
      # make dictionary for renaming headers
      # format: {original : new} or {metadata_formatter : gisaid_format}
      gisaid_rename_headers = {"gisaid_virus_name" : "covv_virus_name", "org_location" : "covv_location", "additional_host_information" : "covv_add_host_info", "gisaid_submitter" : "submitter", "collection_date" : "covv_collection_date", "seq_platform" : "covv_seq_technology", "host" : "covv_host", "assembly_method" : "covv_assembly_method", self.assembly_mean_coverage_column_name : "covv_coverage", "collecting_lab" : "covv_orig_lab", "collecting_lab_address" : "covv_orig_lab_addr", "submitting_lab" : "covv_subm_lab", "submitting_lab_address" : "covv_subm_lab_addr", "authors" : "covv_authors", "purpose_of_sequencing" : "covv_sampling_strategy", "patient_gender" : "covv_gender", "patient_age" : "covv_patient_age", "patient_status" : "covv_patient_status", "specimen_source" : "covv_specimen", "outbreak" : "covv_outbreak", "last_vaccinated" : "covv_last_vaccinated", "treatment" : "covv_treatment", "consortium" : "covv_consortium"}
      
    elif self.organism == "mpox":
      # add additional mpox-specific columns
      gisaid_metadata["pox_passage"] = "original"
      
      # make dictionary for renaming headers
      # format: {original : new} or {metadata_formatter : gisaid_format}
      gisaid_rename_headers = {"gisaid_virus_name" : "pox_virus_name", "org_location" : "pox_location", "gisaid_submitter" : "submitter", "passage_details" : "pox_passage", "collection_date" : "pox_collection_date", "seq_platform" : "pox_seq_technology", "host" : "pox_host", "assembly_method" : "pox_assembly_method", self.assembly_mean_coverage_column_name : "pox_coverage", "collecting_lab" : "pox_orig_lab", "collecting_lab_address" : "pox_orig_lab_addr", "submitting_lab" : "pos_subm_lab", "submitting_lab_address" : "pox_subm_lab_addr", "authors" : "pox_authors", "purpose_of_sequencing" : "pox_sampling_strategy", "patient_gender" : "pox_gender", "patient_age" : "pox_patient_age", "patient_status" : "pox_patient_status", "specimen_source" : "pox_specimen_source", "outbreak" : "pox_outbreak", "last_vaccinated" : "pox_last_vaccinated", "treatment" : "pox_treatment"}

    gisaid_metadata.drop(["continent", "country", "state", "county"], axis=1, inplace=True)

    # replace any empty/NA values for age, status, and gender with "unknown"
    # regex expression '^\s*$' searches for blank strings
    gisaid_metadata["patient_age"] = gisaid_metadata["patient_age"].replace(r'^\s*$', "unknown", regex=True)
    gisaid_metadata["patient_age"] = gisaid_metadata["patient_age"].fillna("unknown")
    gisaid_metadata["patient_gender"] = gisaid_metadata["patient_gender"].replace(r'^\s*$', "unknown", regex=True)
    gisaid_metadata["patient_gender"] = gisaid_metadata["patient_gender"].fillna("unknown")
    gisaid_metadata["patient_status"] = gisaid_metadata["patient_status"].replace(r'^\s*$', "unknown", regex=True)
    gisaid_metadata["patient_status"] = gisaid_metadata["patient_status"].fillna("unknown")
        
 
    self.logger.debug("TABLE:Now preparing the command to rewrite the header of every fasta file to the preferred format")
    gisaid_metadata["fn"] = gisaid_metadata["submission_id"] + "_gisaid.fasta"
    assembly_tuples = list(zip(self.table[self.assembly_fasta_column_name], gisaid_metadata["fn"], gisaid_metadata["gisaid_virus_name"]))
    
    gisaid_metadata.drop(["submission_id"], axis=1, inplace=True)

    self.logger.debug("TABLE:Writing GISAID metadata out to a file")
    gisaid_metadata.rename(columns=gisaid_rename_headers, inplace=True)
    gisaid_metadata.to_csv(self.output_prefix + "_gisaid_metadata.csv", sep=',', index=False)  
    
    for oldname, newname, virus_name in assembly_tuples:
      assembly_rename_command = "gcloud storage cp " + oldname + " ./" + newname
      self.logger.debug("TABLE:Running command: " + assembly_rename_command)
      try:
        subprocess.run(assembly_rename_command, shell=True, check=True)
      except:
        self.logger.error("TABLE:Error: non-zero exit code when copying files to working directory")
        sys.exit(1)
      
      sed_command = "sed -i '1s|.*|>" + virus_name + "|' " + newname
      self.logger.debug("TABLE:Running command: " + sed_command)
      try:
        subprocess.run(sed_command, shell=True, check=True)
      except:
        self.logger.error("TABLE:Error: non-zero exit code when rewriting assembly header")
        sys.exit(1)
    
    self.logger.debug("TABLE:Concatenating GISAID fasta files")
    cat_command = "cat *_gisaid.fasta > " + self.output_prefix + "_gisaid_combined.fasta"
    try:
      subprocess.run(cat_command, shell=True, check=True)
    except:
      self.logger.error("TABLE:Error: non-zero exit code when concatenating fasta files")
      sys.exit(1)
    
    self.logger.debug("TABLE:GISAID metadata preparation complete")

  def process_table(self):
    self.split_metadata()
    self.extract_samples()
    self.create_standard_variables()
    self.perform_quality_check()
    self.remove_nas()
    
    if self.table.empty:
      self.logger.error("TABLE:ENDING PROCESS! No samples were found in the table after extraction and cleaning. Check the input table and/or the excluded samples table and try again.")
      sys.exit(1)
    
    
    self.logger.debug("TABLE:Now creating metadata files")
    if not self.skip_ncbi:
      self.logger.debug("TABLE:NCBI submission NOT skipped, now preparing data for NCBI")
    
      self.make_biosample_csv()
      self.make_sra_csv()
      if self.organism == "sars-cov-2":
        self.make_genbank_csv()
      elif self.organism == "mpox":
        self.make_bankit_src()
    
      self.logger.debug("TABLE:NCBI metadata prepared")
    
    if self.organism != "flu":
      self.logger.debug("TABLE:Creating GISAID metadata")
      self.make_gisaid_csv()
    
    self.logger.debug("TABLE:Metadata tables made")
    
    
    
