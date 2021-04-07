
FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt


RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 5000

CMD [ "python", "app.py","--host=0.0.0.0" ]