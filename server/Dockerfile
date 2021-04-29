FROM python:3.7

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt 

EXPOSE 80

COPY ./ /app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]