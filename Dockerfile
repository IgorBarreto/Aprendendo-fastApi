FROM python:slim-buster

WORKDIR /usr/scr/app

COPY requirements.txt ./

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY .  . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
