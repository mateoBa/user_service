FROM python

RUN mkdir -p /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . /code
CMD ["python", "./service.py"]
