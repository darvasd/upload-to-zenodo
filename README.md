# upload-to-zenodo

A simple, stupid, quick and dirty script to batch upload papers to [Zenodo](http://zenodo.org).

## What is Zenodo?
[Zenodo](http://zenodo.org) is a free, open-source research repository, containing papers, but also data sets and software. 

## Quick start

_You don't want to accidentally flood your real Zenodo account with dummy submissions. We don't want that either. That's why by default the script `upload_to_zenodo.py` uses the sandbox of Zenodo. When you are done with experimenting, just replace `sandbox.zenodo.org` with `zenodo.org` in that script._

1. Get a _Personal access token_ at https://zenodo.org/account/settings/applications/. The `deposit:write` is enough: to be on the safe side, the script does not publish the uploaded papers, the _Publish_ button has to be pushed manually. (Once a document is published on Zenodo, the attached files cannot be modified.)
1. If you would like to group all your uploads to a Zenodo _Comunity_ (that may represent your conference or conference series), [create it](https://zenodo.org/communities/new/) and note its ID. 
1. Create a template JSON describing your submissions. Check the [documentation](https://zenodo.org/dev#restapi-rep) (Representations > Deposition metadata) for details about it.
   - Use `{key-name}` for parts that are different for each submission.
   - An example template and some example deposition metadata files can be found in the example folder.
   - The JSON description of any submitted document can be checked by clicking on the JSON link in the Export panel (or by checking the `https://zenodo.org/record/{ID}/export/json` URL.)
1. Create a CSV file that describes the parts that are different for each submission.
   - The `{key-name}` strings of the template will be replaced by the values from the colmn having `key-name` as header in the CSV file.
   - The CSV file should contain a `FILENAME` column, describing the name of the file created by substituting the values from the given row to the template.
1. Execute the script `fill_template.py` to generate the descriptors (deposition metadata) for each submission.
	- Usage: `fill_template.py <template_filename> <data_filename>`, where `<template_filename>` is the name (path) of the template file, and `<data_filename>` is the name (path) of the CSV data file.
1. Copy the PDF files to be uploaded to the folder where you have previously generated JSON descriptors.
   - The PDF file (paper) that belongs to `xyz.json` is `xyz.pdf`.
1. Execute the script `upload_to_zenodo.py` to upload your submissions.
   - Usage: `upload_to_zenodo.py <token> <directory>`, where `<token>` is your personal access token, and `<directory>` is the directory that contains the JSON and PDF files to be uploaded.
1. Go to the [Upload page](https://zenodo.org/deposit), check and publish your submissions.


## Current status
The scripts are in very early phase. Especially error handling and documentation need more work. But we needed this script quickly...