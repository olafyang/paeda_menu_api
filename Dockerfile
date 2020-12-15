FROM amazon/aws-lambda-python:3.8

WORKDIR /var/task/

COPY . /var/task/

RUN pip install bs4 requests PyPDF2 --target=./

CMD [ "/var/task/lambda_funct.handler" ]