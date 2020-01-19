from PIL import Image, ImageOps
import pytesseract
from bs4 import BeautifulSoup as bs
import difflib
import re
import io
import shutil
from io import StringIO,BytesIO

wordToSearch = "Cash"
imgFilePath="./first.png"


class Output:
    BYTES = 'bytes'
    DATAFRAME = 'data.frame'
    DICT = 'dict'
    STRING = 'string'


def parse_hocr(search_terms=None, hocr_file=None, regex=None):
    """Parse the hocr file and find a reasonable bounding box for each of the strings
    in search_terms.  Return a dictionary with values as the bounding box to be used for 
    extracting the appropriate text.

    inputs:
        search_terms = Tuple, A tuple of search terms to look for in the HOCR file.

    outputs:
        box_dict = Dictionary, A dictionary whose keys are the elements of search_terms and values
        are the bounding boxes where those terms are located in the document.
    """
    # Make sure the search terms provided are a tuple.
    if not isinstance(search_terms,tuple):
        raise ValueError('The search_terms parameter must be a tuple')

    # Make sure we got a HOCR file handle when called.
    if not hocr_file:
        raise ValueError('The parser must be provided with an HOCR file handle.')

    # Open the hocr file, read it into BeautifulSoup and extract all the ocr words.
    #hocr = open(hocr_file)

    
        # assume bytes_io is a `BytesIO` object
    byte_str = hocr_file.read()

    # Convert to a "unicode" object
    hocr = byte_str.decode('UTF-8')  # Or use the encoding you expect
    soup = bs(hocr,'html.parser')
    words = soup.find_all('span',class_='ocrx_word')
    result = dict()
    # Loop through all the words and look for our search terms.        
    for word in words:
        w = word.get_text().lower()
        for s in search_terms:
            # If the word is in our search terms, find the bounding box
            if len(w) > 1 and difflib.SequenceMatcher(None, s, w).ratio() > .5:
                bbox = word['title'].split(';')
                bbox = bbox[0].split(' ')
                bbox = tuple([int(x) for x in bbox[1:]])
                # Update the result dictionary or raise an error if the search term is in there twice.
                if s not in result.keys():
                    result.update({s:bbox})
            else:
                pass
    return result 

def runOCR(wordToSearch="Total",imgFilePath="first"):
    wordToSearch = wordToSearch
    imgFilePath="./" +  imgFilePath + ".png"
    imageObject  = Image.open(imgFilePath)
    hocr = pytesseract.image_to_pdf_or_hocr(imgFilePath, extension='hocr')
    #print(hocr)
    hocr = io.BytesIO(hocr) #https://stackoverflow.com/questions/141449/how-do-i-wrap-a-string-in-a-file-in-python

    #print(parse_hocr(("Other",),hocr))
    dictionary = parse_hocr((wordToSearch,),hocr)

    x0= dictionary[wordToSearch][0]
    y0 = dictionary[wordToSearch][1] 
    x1 = dictionary[wordToSearch][2]
    y1 =dictionary[wordToSearch][3]

    X0 = x1
    Y0 = y0 
    X1 = imageObject.size[0]  #width
    Y1 = y1





    cropped = imageObject.crop((X0,Y0-4,X1,Y1+4))
    bordered = ImageOps.expand(cropped, border=8, fill=(255,255,255))

    extractedText = pytesseract.image_to_string(bordered,output_type=Output.DICT,config="")['text']
    bordered.show()
    print ("text " + extractedText + " ///END")
    response = []
    for item in re.findall(r'((\d{1,3})(,\d{3})*(\.\d+)?)', extractedText):
        response.append(item[0])
    #print(pytesseract.image_to_string(cropped,output_type=Output.DICT))
    return "§".join(response)


    #rint ("hello world")
if __name__ == "__main__":
    runOCR()