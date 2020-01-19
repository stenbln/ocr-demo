from PIL import Image, ImageOps
import pytesseract
from bs4 import BeautifulSoup as bs
import difflib
import re
import io
import shutil
from io import StringIO,BytesIO
import json 

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
    lines = soup.findAll('span',class_='ocr_line')
    words=[]
    result=dict()
    for line in lines:
        #print("linija "+str(line))



        spans = line.findAll('span',class_='ocrx_word')
        text = [span.text for span in spans]

        for index,span in enumerate(spans):
            numberAlreadyEncoutered=False
            if not re.search(r'((\d{1,3})(,\d{3})*(\.\d+)?)', str(span.getText())):
                #numberAlreadyEncoutered = True
                print ("doesnt matches !!!!!!!@#!@#!@#!@#!@#!@#!@#!@##@!@#!@#" + str(span.getText()))
                bbox = span['title'].split(';')
                bbox = bbox[0].split(' ')
                bbox = tuple([int(x) for x in bbox[1:]])
            

      

        #print("bbbbbbbbox "+str(bbox))


        
        text=' '.join(text)
        print(text)
        #text= ''.join([i for i in text if not i.isdigit()])
        words.append(text.lower())
        if text not in result.keys():
            result.update({text.lower():bbox})
    print("words are the following " + str(words))
    print("resultat is important" + str(result))

    #words is an arry of detected lowered strings per line
    #result is a dictionary where keys are .lowered lines from the words array and values are bounding boxes from the last word which is not number!
    #filteredresults is a dictionary where key is a matched search item e.g. Cash and value is the bounding box

    filteredResults=dict()
    for word in words:
        
        #w = word.lower()
        for s in search_terms:
            # If the word is in our search terms, find the bounding box
            
           
            #w=''.join([i for i in w if not i.isdigit()])
           
            stringToMatch = ''.join([i for i in word if not i.isdigit()   ])
            stringToMatch=stringToMatch.replace(",","")
            stringToMatch=stringToMatch.strip()
            print("string TO match-" + stringToMatch)
            print("search item-", s)
            if len(word) > 1 and difflib.SequenceMatcher(None, s, stringToMatch).ratio() > .7:
                print("found a match-" + word)
                
                if word not in filteredResults.keys():
                    filteredResults.update({s:result[word]})
                # Update the result dictionary or raise an error if the search term is in there twice.
            else:
                pass

    print("filtered result " + str(filteredResults))
    #price = [item.findAll('span',class_='ocrx_word').text for item in soup.findAll('span',class_='ocr_line') ] 
    #print (str(price))
    #result = dict()
    # Loop through all the words and look for our search terms.  
    #lines = words    
    #for line in lines:
     #   marked = line.find_all('span',class_='ocrx_word',recursive=False)


    #print("mark my words " + marked.text)

    return filteredResults 

def runOCR(wordToSearch="Cash",imgFilePath="second"):
    wordToSearch = wordToSearch
    imgFilePath="./" +  imgFilePath + ".png"
    imageObject  = Image.open(imgFilePath)
    hocr = pytesseract.image_to_pdf_or_hocr(imgFilePath, extension='hocr')
    #print(hocr)
    print("image file path " + imgFilePath)
    hocr = io.BytesIO(hocr) #https://stackoverflow.com/questions/141449/how-do-i-wrap-a-string-in-a-file-in-python

    #print(parse_hocr(("Other",),hocr))
    dictionary = parse_hocr((wordToSearch,),hocr)
    print("sjsojdojdosjsodj" + str(dictionary)+ str(any(dictionary)))
    if(any(dictionary)):
        for key, value in dictionary.items():
            print("value sds" + str(key) + str(value))
            x0= value[0]
            y0 = value[1] 
            x1 = value[2]
            y1 =value[3]

            X0 = x1
            Y0 = y0 
            X1 = imageObject.size[0]  #width
            Y1 = y1





        cropped = imageObject.crop((X0,Y0-6,X1,Y1+6))
        bordered = ImageOps.expand(cropped, border=9, fill=(255,255,255))

        extractedText = pytesseract.image_to_string(bordered,output_type=Output.DICT,config="")['text']
        #bordered.show()
        print ("text " + extractedText + " ///END")
        response = []
        for item in re.findall(r'((\d{1,3})(,\d{3})*(\.\d+)?)', extractedText):
            response.append(item[0])
        #print(pytesseract.image_to_string(cropped,output_type=Output.DICT))
        for key, value in dictionary.items():
            dictionary[key] = response
            #dictionary[wordToSearch]=response
    return dictionary
    



    


    #rint ("hello world")
if __name__ == "__main__":
    runOCR()