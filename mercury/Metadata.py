class Metadata:
  """This class controls the various different metadata requirements
  """
  
  def __init__(self, logger, organism, skip_ncbi, assembly_mean_coverage_column_name):
    self.logger = logger
    self.organism = organism
    self.skip_ncbi = skip_ncbi
    self.assembly_mean_coverage_column_name = assembly_mean_coverage_column_name
    
  def sc2_biosample_metadata(self):
    biosample_required = ["submission_id", "bioproject_accession", "organism", "collecting_lab", "collection_date", "country", "state", "host_sci_name", "host_disease", "isolation_source"]
    biosample_optional = ["isolate", "treatment", "gisaid_accession", "gisaid_virus_name", "patient_age", "patient_gender", "purpose_of_sampling", "purpose_of_sequencing"]
    return biosample_required, biosample_optional

  def sc2_gisaid_metadata(self):     
    gisaid_required = ["gisaid_submitter", "submission_id", "collection_date", "continent", "country", "state", "host", "seq_platform", "assembly_method", self.assembly_mean_coverage_column_name, "collecting_lab", "collecting_lab_address", "submitting_lab", "submitting_lab_address", "authors"]
    gisaid_optional = ["gisaid_virus_name", "additional_host_information", "county", "purpose_of_sequencing", "patient_gender", "patient_age", "patient_status", "specimen_source", "outbreak", "last_vaccinated", "treatment", "consortium"]
    return gisaid_required, gisaid_optional

  def mpox_biosample_metadata(self):
    biosample_required = ["submission_id", "organism", "collecting_lab", "collection_date",  "country", "state", "host_sci_name", "host_disease", "isolation_source", "lat_lon", "bioproject_accession", "isolation_type"]
    biosample_optional = ["sample_title", "strain", "isolate", "culture_collection", "genotype", "patient_age", "host_description", "host_disease_outcome", "host_disease_stage", "host_health_state", "patient_gender", "host_subject_id", "host_tissue_sampled", "passage_history", "pathotype", "serotype", "serovar", "specimen_voucher", "subgroup", "subtype", "description"] 
    return biosample_required, biosample_optional
  
  def mpox_gisaid_metadata(self):
    gisaid_required = ["gisaid_submitter", "gisaid_virus_name", "submission_id", "collection_date", "continent", "country", "state", "host", "seq_platform", "assembly_method", self.assembly_mean_coverage_column_name, "collecting_lab", "collecting_lab_address", "submitting_lab", "submitting_lab_address", "authors"]
    gisaid_optional = ["county", "purpose_of_sequencing", "patient_gender", "patient_age", "patient_status", "specimen_source", "outbreak", "last_vaccinated", "treatment"]
    return gisaid_required, gisaid_optional

  def flu_biosample_metadata(self):
    biosample_required = ["submission_id", "organism", "collected_by", "collection_date", "geo_loc_name", "host", "host_disease", "isolation_source", "lat_lon"]
    biosample_optional = ["sample_title", "isolation_type", "bioproject_accession", "attribute_package", "strain", "isolate", "culture_collection", "genotype", "host_age", "host_description", "host_disease_outcome", "host_disease_stage", "host_health_state", "host_sex", "host_subject_id", "host_tissue_sampled", "passage_history", "pathotype", "serotype", "serovar", "specimen_voucher", "subgroup", "subtype", "description"] 
    return biosample_required, biosample_optional

  def bankit_metadata(self):
    bankit_required = ["submission_id", "collection_date", "country", "host"]
    bankit_optional = ["isolate", "isolation_source"]
    return bankit_required, bankit_optional
    
  def sra_metadata(self):
    self.logger.debug("METADATA:Retrieving SRA metadata")
    sra_required = ["bioproject_accession", "submission_id", "library_id", "organism", "isolation_source", "library_strategy", "library_source", "library_selection", "library_layout", "instrument_model", "filetype"]
    sra_optional = ["title", "design_description", "amplicon_primer_scheme", "amplicon_size", "assembly_method", "dehosting_method", "submitter_email"]
    
    # note: the flu metadata formatter currently uses "platform" instead of "seq_platform" because it uses the Terra_2_NCBI Pathogen BioSample formatter.
    if self.organism == "flu":
      sra_required.append("platform")
    else:
      sra_required.append("seq_platform")
    return sra_required, sra_optional

  def genbank_metadata(self):  
    genbank_required = ["submission_id", "country", "host_sci_name", "collection_date", "isolation_source", "biosample_accession", "bioproject_accession"]
    genbank_optional = ["isolate", "state"]
    return genbank_required, genbank_optional

  def get_metadata(self):
    """This function retrieves the metadata requirements for the organism
    """
    self.logger.debug("METADATA:Retrieving metadata requirements")
    if not self.skip_ncbi:
      self.logger.debug("METADATA:NCBI submission is not skipping, retrieving NCIB-specific metadata requirements for " + self.organism)
      if self.organism == "sars-cov-2":
        biosample_required, biosample_optional = self.sc2_biosample_metadata()
        sra_required, sra_optional = self.sra_metadata()
        genbank_required, genbank_optional = self.genbank_metadata()
        
        required_metadata = [biosample_required, sra_required, genbank_required]
        optional_metadata = [biosample_optional, sra_optional, genbank_optional]
        self.logger.debug("METADATA:NCBI-specific metadata retrieved for " + self.organism)
      elif self.organism == "flu":
        biosample_required, biosample_optional = self.flu_biosample_metadata()
        sra_required, sra_optional = self.sra_metadata()
        
        required_metadata = [biosample_required, sra_required]
        optional_metadata = [biosample_optional, sra_optional]
        self.logger.debug("METADATA:NCBI-specific metadata retrieved for " + self.organism)
      elif self.organism == "mpox":
        biosample_required, biosample_optional = self.mpox_biosample_metadata()
        sra_required, sra_optional = self.sra_metadata()
        bankit_required, bankit_optional = self.bankit_metadata()
        
        required_metadata = [biosample_required, sra_required, bankit_required]
        optional_metadata = [biosample_optional, sra_optional, bankit_optional]
        self.logger.debug("METADATA:NCBI-specific metadata retrieved for " + self.organism)
      else:
        self.logger.debug("METADATA:NCBI-specific metadata could not be retrieved for " + self.organism)
      
    else:
      self.logger.debug("METADATA:NCBI submission is skipped, no NCBI-specific metadata was retrieved")

    self.logger.debug("METADATA:Retrieving GISAID metadata requirements for " + self.organism)
    if self.organism == "sars-cov-2":
      gisaid_required, gisaid_optional = self.sc2_gisaid_metadata()
      
      required_metadata = required_metadata + [gisaid_required]
      optional_metadata = optional_metadata + [gisaid_optional] 
      self.logger.debug("METADATA:GISAID metadata retrieved successfully for " + self.organism)
    elif self.organism == "mpox":
      gisaid_required, gisaid_optional = self.mpox_gisaid_metadata()
     
      required_metadata = required_metadata + [gisaid_required]
      optional_metadata = optional_metadata + [gisaid_optional]
      self.logger.debug("METADATA:GISAID metadata retrieved successfully for " + self.organism)
    else:
      self.logger.debug("METADATA:GISAID metadata could not be retrieved for " + self.organism)
    
    self.logger.debug("METADATA:Metadata requirements retrieved successfully")
    return [required_metadata, optional_metadata]
  