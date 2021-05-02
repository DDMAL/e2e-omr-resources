import argparse
import csv


def retrieve_text(csvpath):
    csvfile = open(csvpath, 'r')
    csv_reader = csv.reader(csvfile, delimiter=',')
    # Variable initialization
    prev_folio = 'folio' # the header of the folio column
    mss_text = {}
    folio_text = ""
    prev_chant = ""
    # Move through the folios and extract the text
    for row in csv_reader:
        folio = row[2]
        chant = row[14]
        # If we are in the same folio as in the previous row,
        # just add the corresponding chant of the folio_text
        if folio == prev_folio:
            folio_text = folio_text + "\n" + chant
        # If we changed folio, 
        # 1. Add the complete text of the previos folio to the MSS Text dictionary
        # 2. And start a new text (folio_text) with the last chant
        # the previous folio and the first chant of the new folio
        else:
            mss_text[prev_folio] = folio_text
            folio_text = prev_chant + "\n" + chant
        # Update the folio number for next iteration
        prev_folio = folio
        prev_chant = chant
    # When it finishes, add the computed folio_text 
    # (the text of the last folio) to the dictionary
    mss_text[prev_folio] = folio_text
    # And close the file
    csvfile.close()

    mss_text.pop('folio')
    for folio in mss_text.keys():
        with open(folio + '.txt', mode='w') as file:
            file.write(mss_text[folio])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program takes the CSV file from Cantus DB and returns a set of text files, each containing the text of the chants in each folio.")
    parser.add_argument('cantusdb_csvfile', help="Cantus Database CSV file from which the text of the chants on each folio is extracted.")
    args = parser.parse_args()

    retrieve_text(args.cantusdb_csvfile)