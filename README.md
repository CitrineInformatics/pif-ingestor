# pif-ingestor

Script to ingest common data formats to citrination.
It uses an extention architecture to mport and evaluate converters defined in other pacakages, e.g. [pif-dft](https://github.com/CitrineInformatics/pif-dft) and [sparks-pif-converters](https://github.com/CitrineInformatics/sparks-pif-converters).

## Installation

Install this ingestor and all known public converters:
```
$ pip install pif-ingestor[all]
```
This will place an executable `pif-ingestor` in your bin directory (or the bin directory of your virtualenv).

## Usage
```
$ pif-ingestor -h
usage: pif-ingestor [-h] [-d DATASET] [-f FORMAT] [--tags TAGS [TAGS ...]]
                    [-l LICENSE] [-c CONTACT] [--log LOG_LEVEL]
                    [--args CONVERTER_ARGUMENTS]
                    path

Import data files to Citrination

positional arguments:
  path                  Location of the file or directory to ingestor

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        Dataset ID into which to upload PIFs
  -f FORMAT, --format FORMAT
                        Format of data to ingestor
  --tags TAGS [TAGS ...]
                        Tags to add to PIFs
  -l LICENSE, --license LICENSE
                        License to attach to PIFs
  -c CONTACT, --contact CONTACT
                        Contact information
  --log LOG_LEVEL       Contact information
  --args CONVERTER_ARGUMENTS
                        Arguments to pass to converter (as json dictionary)
```

## Examples

Convert a VASP file, generating a quality report, and upload it to datasetID 7:
```
$ pif-ingestor B.hR12 -f dft -d --args='{"quality_report" : true}'
```
