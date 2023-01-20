FROM tiangolo/uvicorn-gunicorn-fastapi
ENV TIMEOUT=10000

RUN pip install pymysql
RUN pip install sqlalchemy
RUN pip install pandas
RUN pip install numpy
RUN pip install sendmail
RUN pip install requests 

EXPOSE 80
COPY ./app /app