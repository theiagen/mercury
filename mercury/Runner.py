import mercury.Table as Table
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
    self.logger.info("RUNNER:Found `gcloud storage cp` command, continuing")

  def run(self):
    """This class runs the different parts of Mercury
    """
    self.logger.info("RUNNER:Starting to run Mercury")
    self.logger.debug("RUNNER:Checking for `gcloud storage cp` command")
    
    
    
    