from Table import Table
from Metadata import Metadata
import logging
import subprocess
import sys

class Runner:
  """This class intiates Mercury 
  """
  
  def __init__(self, options):
    logging.basicConfig(encoding='utf-8', level=logging.ERROR, stream=sys.stderr)
    self.logger = logging.getLogger(__name__)
    if options.verbose:
        self.logger.setLevel(logging.INFO)
        self.logger.info("RUNNER:Verbose mode enabled")
    elif options.debug:
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("RUNNER:Debug mode enabled")

    self.input_table = options.input_table
    self.table_name = options.table_name
    self.samplenames = options.samplenames
    self.output_prefix = options.output_prefix
    self.gcp_bucket_uri = options.gcp_bucket_uri
    self.organism = options.organism
    self.skip_ncbi = options.skip_ncbi
    self.skip_county = options.skip_county
    self.usa_territory = options.usa_territory
    self.clearlabs_data = options.using_clearlabs_data
    self.reads_dehosted = options.using_reads_dehosted
    self.vadr_alert_limit = options.vadr_alert_limit
    self.number_n_threshold = options.number_n_threshold
    
    # set the data file names
    self.read1_column_name = "read1_dehosted"
    self.read2_column_name = "read2_dehosted"
    self.assembly_fasta_column_name = "assembly_fasta"
    self.assembly_mean_coverage_column_name = "assembly_mean_coverage"
    
    self.single_end = options.single_end
    
    if self.clearlabs_data:
      self.read1_column_name = "clearlabs_fastq_gz"
      self.assembly_fasta_column_name = "clearlabs_fasta"
      self.assembly_mean_coverage_column_name = "clearlabs_sequencing_depth"
      
    if self.reads_dehosted:
      self.read1_column_name = "reads_dehosted"
      
    if self.organism not in ["sars-cov-2", "flu", "mpox"]:
      self.logger.error("RUNNER:Error: Organism not recognized")
      sys.exit(1)

  def check_gcloud_dependency(self):
    result = subprocess.run(
      ["gcloud", "storage", "cp", "--help"],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
    )
    if result.returncode != 0:
      self.logger.error("RUNNER:Error: gcloud storage cp command not found")
      sys.exit(1)
    self.logger.debug("RUNNER:Found `gcloud storage cp` command, continuing")

  def run(self):
    """
    This class orchestrates the different parts of Mercury
    """
    self.logger.info("RUNNER:Starting to run Mercury")
    self.logger.debug("RUNNER:Checking for `gcloud storage cp` command")
    self.check_gcloud_dependency()
    
    self.logger.debug("RUNNER:Gathering metadata")
    
    metadata = Metadata(self.logger, self.organism, self.skip_ncbi, self.assembly_mean_coverage_column_name)
    metadata_list = metadata.get_metadata()      
    
    self.logger.debug("RUNNER:Processing table")
    table = Table(self.logger, self.organism, self.input_table, self.table_name, self.samplenames, self.skip_county, 
                  self.skip_ncbi, self.usa_territory, metadata_list, self.vadr_alert_limit, self.number_n_threshold, 
                  self.assembly_fasta_column_name, self.output_prefix, self.gcp_bucket_uri, self.single_end, 
                  self.read1_column_name, self.assembly_mean_coverage_column_name, 
                  self.authors, self.bioproject_accession, self.continent, self.country, self.host_disease, 
                  self.isolation_source, self.library_selection, self.library_source, self.library_strategy, 
                  self.purpose_of_sequencing, self.state, self.submitting_lab, self.submitting_lab_address, 
                  self.amplicon_primer_scheme, self.amplicon_size, self.instrument_model, self.library_layout, self.seq_platform, 
                  self.gisaid_submitter, self.submitter_email, self.read2_column_name)
    table.process_table()
      
    self.logger.info("RUNNER:Done!")