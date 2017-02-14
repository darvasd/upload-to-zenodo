import json
import requests
import os
import sys
import codecs

BASE_URL = "https://sandbox.zenodo.org" # TODO: once you are sure about what you are doing, remove the "sandbox." part
TOKEN = ""

def upload(metadata, pdf_path):
    if not _is_valid_json(metadata):
        return

    # Create new paper submission
    url = "{base_url}/api/deposit/depositions/?access_token={token}".format(base_url=BASE_URL, token=TOKEN)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=metadata, headers=headers)
    #print(response.text)
    if response.status_code > 210:
        print("Error happened during submission, status code: " + str(response.status_code))
        return

    # Get the submission ID
    submission_id = json.loads(response.text)["id"]

    # Upload the file
    url = "{base_url}/api/deposit/depositions/{id}/files?access_token={token}".format(base_url=BASE_URL, id=str(submission_id), token=TOKEN)
    upload_metadata = {'filename': 'paper.pdf'}
    files = {'file': open(pdf_path, 'rb')}
    response = requests.post(url, data=upload_metadata, files=files)
    #print(response.text)
    if response.status_code > 210:
        print("Error happened during file upload, status code: " + str(response.status_code))
        return
    
    print("{file} submitted with submission ID = {id} (DOI: 10.5281/zenodo.{id})".format(file=pdf_path,id=submission_id))    
    # The submission needs an additional "Publish" step. This can also be done from a script, but to be on the safe side, it is not included. (The attached file cannot be changed after publication.)
    
    
def batch_upload(directory):
    for metadata_file in os.listdir(directory):
        metadata_file = os.path.join(directory, metadata_file)
        if metadata_file.endswith(".json"):
            pdf_file = metadata_file.replace(".json",".pdf")
            if os.path.isfile(pdf_file):
                print("Uploading %s & %s" % (metadata_file, pdf_file))
                with codecs.open(metadata_file, 'r', "utf-8") as f:
                    metadata = f.read()
                    # Re-encoding in order to support UTF-8 inputs
                    metadata = json.dumps(json.loads(metadata), ensure_ascii=True)
                    print(metadata)
                upload(metadata, pdf_file)
            else:
                print("The file %s might be a submission metadata file, but %s does not exist." % (metadata_file, pdf_file))
           
           
def _is_valid_json(text):
    try:
        json.loads(text)
        return True
    except ValueError as e:
        print('Invalid json: %s' % e)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: upload_to_zenodo.py <token> <directory>")
        print("  The directory contains .json metadata descriptors and .pdf files.")
        exit()
    
    TOKEN = sys.argv[1]
    directory = sys.argv[2]
    if not os.path.isdir(directory):
        print("Invalid directory.")
        exit()
   
    batch_upload(directory)