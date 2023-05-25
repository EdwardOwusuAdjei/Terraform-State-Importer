# Terraform State Parser

This Python script can be used to parse Terraform state files and extract information about the resources and outputs used in the state file.

## Usage

1. Install Python 3.x and ensure that pip is installed.
2. Copy the `state-importer.py` script to your machine.
3. Navigate to the directory where the script is saved.
4. Run the script with the following command: `python state-parser.py [tfstate-file-path] [terraform-file-path]`
5. The parsed state file will be saved as `default.tfstate` in the same directory as the script.

## Script Overview

This script takes in two arguments: the path to the Terraform state file and the path to the Terraform configuration file. The script reads the state file and configuration file and extracts information about the resources and outputs defined in the configuration file.

e.g. `python3 state-importer.py /Users/doe/Downloads/actual.tfstate /Users/doe/somerepo/terraform/api/staging/dataman.tf`

Output:

```
----------
found 7 resources and modules, with names: 
resources:
* dataman
* dataman_apistaging_com
* staging_api_service_account_key
* module.staging_dataman
* dataman-staging
* module.staging_dataman_iam
* staging_dataman_service_account
--------------------------------------------
found 1 outputs, with names: 
output:
- staging_dataman_gcp_key
```

The script uses regular expressions to extract the names of resources and modules from the configuration file. It then searches the state file for blocks that match these names and extracts the relevant information about those blocks.

Finally, the script outputs a new state file that includes only the relevant blocks and outputs. This new state file can be used to share state information with other team members or to keep track of changes to the state over time.