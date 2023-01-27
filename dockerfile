FROM tiangolo/uvicorn-gunicorn-fastapi
ENV TIMEOUT=10000

RUN pip install pymysql
RUN pip install pandas
RUN pip install numpy
RUN pip install sendmail


EXPOSE 80
COPY ./app /app
