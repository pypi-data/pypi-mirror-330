# PredDNAContam

PredDNAContam is a tool to Estimate Within-Species DNA Contamination. 


## Input File Format (CSV)

When using **PredDNAContam**, your input data should be in CSV format with the following columns:

| Column  | Description |
|---------|------------|
| GQ      | Genotype quality |
| DP      | Total read depth |
| AF      | Allele frequency |
| VAF     | Variant allele frequency |

### Example CSV File

The input CSV file should be generated from a VCF (Variant Call Format) file that is produced using HaplotypeCaller from GATK.
The following key features should be extracted from the VCF file for each variant to create the CSV.

```csv
GQ,DP,AF,VAF
20,47,0.5,0.23
60,25,0.5,0.24
23,55,0.5,0.78
```


## Download and Installation

To install PredDNAContam, follow these steps:

1. Download the package
You can download the package from PyPI:

👉 PredDNAContam on PyPI 

🔗 https://pypi.org/project/PredDNAContam/#files

Download the file:
📂 preddnacontam-0.0.4.tar.gz 

2. Extract the package

After downloading, unzip the file:

```
tar -xvzf preddnacontam-0.0.4.tar.gz
cd preddnacontam-0.0.4
```

3. Install the package
Inside the extracted directory, run:

```
pip install .
```

## Running PredDNAContam
1. Modify the configuration file

Navigate to the scripts directory and update config.txt to set the correct paths for your input files, and output directory.

2. Run the tool 
After configuring the paths, execute PredDNAContam:

```
PredDNAContam
```

