# mercury

## Description

### help

```bash
usage: python3 /mercury/mercury/mercury.py <input_table.tsv> <table_name> <samplenames> [<args>]

Mercury prepares and formats metadata for submission to national & international genomic databases

positional arguments:
  input_table
          The table containing the metadata for the samples to be submitted
  table_name
          The name of the first column in the table (A1)
  samplenames
          The sample names to be extracted from the table

optional arguments:
  -h, --help
          show this help message and exit
  -v, --version
          show program's version number and exit
  -o, --output_prefix
          The prefix for the output files
          default="mercury"
  -b, --gcp_bucket_uri
          The GCP bucket URI to store the temporarily store the read files (required)

submission type arguments:
  options that determine submission type

  --organism
          The organism type of the samples in the table
          default="sars-cov-2"
  --skip_ncbi
          Add to skip NCBI metadata preparation; prep only for GISAID submission

submission customization arguments:
  options that customize the submission

  --skip_county
          Add to skip adding county to location in GISAID metadata
  --usa_territory
          Add if the country is a USA territory to use the territory name in the state column
  --using_clearlabs_data
          Add if using Clearlabs-generated data and metrics
  --using_reads_dehosted
          Add if using reads_dehosted instead of clearlabs data
  --single_end
          Add if the data is single-end

quality control arguments:
  options that control quality thresholds

  -a, --vadr_alert_limit
          The maximum number of VADR alerts allowed for SARS-CoV-2 samples
          default=0
  -n, --number_n_threshold
          The maximum number of Ns allowed in SARS-CoV-2 assemblies
          default=5000

logging arguments:
  options that change the verbosity of the stdout logging

  --verbose
          Add to enable verbose logging
  --debug
          Add to enable debug logging; overwrites --verbose
```
