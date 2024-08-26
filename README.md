# mercury

## Description

Mercury prepares and formats metadata and sequencing files **located in GCP buckets** for submission to national & international databases, currently NCBI & GISAID. The default organism (set with `--organism`) is `"sars-cov-2"` although `"mpox"` and `"flu"` are also accepted.

Important note: Mercury was designed to work with metadata tables that were processed after running the TheiaCoV workflows. If you are using a different pipeline, please ensure that the metadata table is formatted correctly.

For all organisms:

1. Required & optional metadata fields are retrieved from the `Metadata.py` file, dependent on the optional `--organism` and `--skip_ncbi` arguments.
2. The input TSV file is read (from the positional `input_table` and `table_name` argument) and the required/optional metadata is extracted for only the samples specified in the postiional `samplenames` argument.
3. The metadata is formatted according to the requirements of each database, dependent on the specified `--organism` argument.
4. If SRA submission is not skipped (if `--skip_ncbi` is indicated), the sequencing read files (fastq files) are uploaded to a Google Cloud Storage bucket (specified by `--gcp_bucket_uri`) for temporary storage until they can be retrieved by NCBI (specifically, SRA) during submission.
5. For BankIt, GenBank, and/or GISAID, The assembly files (fasta files) are concatenated and have the header lines renamed and are available for local download and submission to respective databases.

Default databases by organism:

- `"sars-cov-2"`: BioSample, GenBank, GISAID, SRA
- `"mpox"`: BankIt, BioSample, GISAID, SRA
- `"flu"`: BioSample, SRA

## Installation

### Docker

We highly recommend using the following Docker image to run Mercury:

```bash
docker pull us-docker.pkg.dev/general-theiagen/theiagen/mercury:1.0.8
```

The entrypoint for this Docker image is the Mercury help message. To run this container interactively, use the following command:

```bash
docker run -it --entrypoint=/bin/bash us-docker.pkg.dev/general-theiagen/theiagen/mercury:1.0.8
# Once inside the container interactively, you can run the mercury tool
python3 /mercury/mercury/mercury.py -v
# v1.0.8
```

### Locally with Python

Mercury is not yet available with `pip` or `conda`. To run Mercury in your local command-line environment, install the following dependencies:

- Python 3.9+
- pandas >= 1.4.2
- Google Cloud SDK 479.0.0+ and all its dependencies
- numpy >= 1.22.4

## Outputs

Each organism will produce different output files. See the table below:

| | `<output_name>_bankit_combined.fasta` | `<output_name>.src` | `<output_name>_biosample_metadata.tsv` |`<output_name>_genbank_metadata.tsv` | `<output_name>_genbank_combined.fasta` |`<output_name>_gisaid_metadata.csv` | `<output_name>_gisaid_combined.fasta` |  `<output_name>_sra_metadata.tsv` | `<output_name>_excluded_samples.tsv` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -- |
| organism | BankIt | BankIt | BioSample | GenBank | GenBank | GISAID | GISAID | SRA | N/A |
| `"mpox"` | &check; | &check; | &check; |  |  | &check; | &check; | &check; | &check; |
| `"sars-cov-2"` | | | &check; | &check; | &check; | &check; | &check; | &check; | &check; |
| `"flu"` | | | &check; |  |  | | | &check; | &check; |

## Explanation of Arguments

### Usage & Help Message

```text
usage: python3 /mercury/mercury/mercury.py <input_table.tsv> <table_name> <samplenames> [<args>]

Mercury prepares and formats metadata for submission to national & international genomic databases

positional arguments:
  input_table
          The table containing the metadata for the samples to be submitted
  table_name
          The name of the first column in the table (A1); include the `_id` if data table is downloaded from Terra.bio
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

metadata customization arguments:
  options that customize the metadata configuration

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
  options that control quality thresholds (currently only for SARS-CoV-2 samples)

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

Please contact support@theiagen.com or sage.wright@theiagen.com with any questions
```

### Positional & Required Arguments

To successful run Mercury, these arguments are required.

- `input_table`: The table containing the metadata for the samples to be submitted in TSV format
- `table_name`: The name of the first column in the table (A1) in its entirety
- `samplenames`: The sample names to be extracted from the table (or in other words, the names of the rows in the table) _in a comma-delimited list_
- `--gcp_bucket_uri`: The GCP bucket URI to store the temporarily store the read files (such as `gs://bucket_with_sra_access_permissions`; contact support@theiagen.com if you would like to use the GCP bucket we use for this purpose)

### Optional Arguments

These arguments provide helpful information, or help customize the output file names.

- `-h, --help`: Show the help message and exit
- `-v, --version`: Show the program's version number and exit
- `-o, --output_prefix`: The prefix for the output files (default is `"mercury"`)

### Submission Type Arguments

These arguments change the type of submission Mercury prepares.

- `--organism`: The organism type of **all** the samples in the table (default is `"sars-cov-2"`; options include `"sars-cov-2"`, `"mpox"`, and `"flu"`; contact us if you would like any additional organisms/databases supported)
- `--skip_ncbi`: Add to skip NCBI metadata preparation; prepare metadata and sequencing files only for GISAID submission

### Metadata Customization Arguments

These arguments customize the configuration of the required and/or optional metadata.

- `--skip_county`: Add to skip adding county to location in GISAID metadata
- `--usa_territory`: Add if the country is a USA territory to use the territory name in the state column; this is useful for territories like Puerto Rico (e.g., instead of "North America/USA/Puerto Rico", the location will be "North America/Puerto Rico")
- `--using_clearlabs_data`: Add if using Clearlabs-generated data and metrics
- `--using_reads_dehosted`: Add if using reads_dehosted instead of clearlabs data
- `--single_end`: Add if the data is single-end; this ensures that the `read2` column is not included in the metadata

#### A note on `--using_clearlabs_data` & `--using_reads_dehosted` 

The `--using_clearlabs_data` and `--using_reads_dehosted` arguments change the default values for the `read1_column_name`, `assembly_fasta_column_name`, and `assembly_mean_coverage_column_name` metadata columns. The default values are shown in the table below in addition to what they are changed to depending on what arguments are used.

| Variable | Default Value | with `--using_clearlabs_data` | with `--using_reads_dehosted` | with both `--using_clearlabs_data` **_and_** `--using_reads_dehosted` |
| --- | --- | --- | --- | --- |
| `read1_column_name` | `"read1_dehosted"` | `"clearlabs_fastq_gz"` | `"reads_dehosted"` | `"reads_dehosted"` |
| `assembly_fasta_column_name` | `"assembly_fasta"` | `"clearlabs_fasta"` | `"assembly_fasta"` | `"clearlabs_fasta"` |
| `assembly_mean_coverage_column_name` | `"assembly_mean_coverage"` | `"clearlabs_assembly_coverage"` | `"assembly_mean_coverage"` | `"clearlabs_assembly_coverage"` |

### Quality Control Arguments

These arguments are currently only implemented for SARS-CoV-2. If any samples do not meet the quality thresholds, they will not be submitted to the respective databases and will be found in the `<output_prefix>_excluded_samples.tsv` file. If provided for other organisms, they will be ignored.

- `--vadr_alert_limit`: The maximum number of VADR alerts allowed for SARS-CoV-2 samples (default is `0`)
- `--number_n_threshold`: The maximum number of Ns allowed in SARS-CoV-2 assemblies (default is `5000`)

### Logging Arguments

These arguments control the amount of logging that is output to the console.

- `--verbose`: Add to enable verbose logging
- `--debug`: Add to enable debug logging; overwrites `--verbose`

----------

Happy submissions!
