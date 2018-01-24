import sys
import csv
import os.path


def fill_template(template_filename, data_filename):
    # Reading the template
    with open(template_filename,"r") as template_file:
        template = template_file.read()

    # Creating the files based on the template and the data descriptor CSV
    with open(data_filename,"r", encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            output_filename = row["FILENAME"]
            print("Writing %s..." % output_filename)
            
            # Performing replacements
            filled_template = template
            for column in csv_reader.fieldnames:
                if column != "FILENAME":
                    filled_template = filled_template.replace("{%s}" % column, row[column])
                    print(("    {%s} = %s" % (column, row[column])).encode().decode('cp850'))
                    
            # Write to output file
            with open(output_filename, "w", encoding='utf-8') as output_file:
                output_file.write(filled_template)
                
                
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: fill_template.py <template_filename> <data_filename>")
        exit()
    
    template_filename = sys.argv[1] # e.g. "template.json"
    if not os.path.isfile(template_filename):
        print("Invalid template filename.")
        exit()
    
    data_filename = sys.argv[2] # e.g. "data.csv"
    if not os.path.isfile(data_filename):
        print("Invalid data filename.")
        exit()
    
    fill_template(template_filename, data_filename)