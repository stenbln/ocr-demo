FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
 
RUN apt-get update -y
RUN apt install tesseract-ocr -y


COPY . .
EXPOSE 80

#CMD [ "python", "./code.py" ]
CMD ["python", "app.py" ]

#CMD tail -f /dev/null
