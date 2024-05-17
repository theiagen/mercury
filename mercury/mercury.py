#!/usr/bin/env python3
import CheckInputs
import argparse
from __init__ import __VERSION__
from Runner import Runner

def main():
  parser = argparse.ArgumentParser(
    prog = "mercury",
    description = "Mercury prepares and formats metadata for submission to national & international genomic databases",
    usage = "python3 /mercury/mercury/mercury.py <input_table.tsv> [<args>]",
    epilog = "Please contact support@theiagen.com with any questions",
    formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=10)
  )
  parser.add_argument("-v", "--version", action="version", version=str(__VERSION__))

  parser.add_argument("input_table",
                      help="The table containing the metadata for the samples to be submitted", type=CheckInputs.is_table_valid)
  parser.add_argument("table_name",
                      help="The name of the first column in the table (A1)", type=str)
  parser.add_argument("samplenames",
                      help="The sample names to be extracted from the table", type=CheckInputs.is_comma_delimited_list)
  parser.add_argument("-o", "--output_prefix",
                      help="The prefix for the output files", type=str)
  parser.add_argument("-b", "--gcp_bucket_uri",
                      help="The GCP bucket URI to store the temporarily store the read files", type=str)
  
  submission_type_arguments = parser.add_argument_group("submission type arguments", "options that determine submission type")
  submission_type_arguments.add_argument("-g", "--organism", 
                                         help="The organism type of the samples in the table\ndefault=\"sars-cov-2\"", default="sars-cov-2", metavar="\b",type=str)
  submission_type_arguments.add_argument("-s", "--skip_ncbi", 
                                         help="Add to skip NCBI metadata preparation; prep only for GISAID submission", action="store_true", default=False)
  
  customization_arguments = parser.add_argument_group("submission customization arguments", "options that customize the submission")
  customization_arguments.add_argument("-c", "--skip_county",
                                       help="Add to skip adding county to location in GISAID metadata", action="store_true", default=False)
  customization_arguments.add_argument("-u", "--usa_territory",
                                       help="Add if the country is a USA territory to use the territory name in the state column", action="store_true", default=False)
  customization_arguments.add_argument("-d", "--using_clearlabs_data",
                                       help="Add if using Clearlabs-generated data and metrics", action="store_true", default=False)
  customization_arguments.add_argument("-r", "--using_reads_dehosted",
                                       help="Add if using reads_dehosted instead of clearlabs data", action="store_true", default=False)
  
  qc_arguments = parser.add_argument_group("quality control arguments", "options that control quality thresholds")
  qc_arguments.add_argument("-a", "--vadr_alert_limit",
                            help="The maximum number of VADR alerts allowed for SARS-CoV-2 samples\ndefault=0", default=0, type=int)
  qc_arguments.add_argument("-n", "--number_n_threshold",
                            help="The maximum number of Ns allowed in SARS-CoV-2 assemblies\ndefault=5000", default=5000, type=int)

  logging_arguments = parser.add_argument_group("logging arguments", "options that change the verbosity of the stdout logging")
  logging_arguments.add_argument("--verbose",
                                 help="Add to enable verbose logging", action="store_true", default=False)
  logging_arguments.add_argument("--debug",
                                  help="Add to enable debug logging; overwrites --verbose", action="store_true", default=False)

  options = parser.parse_args()
  
  parse = Runner(options)
  parse.run()

if __name__ == "__main__":
  main()