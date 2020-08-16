FROM python:3.7-alpine
MAINTAINER "Manny E <manny@knowi.com>"
COPY ../knowi-okta-flask-docker1 /src
WORKDIR /src
RUN pip install -r requirements.txt
ENV KNOWI_CUSTOMER_TOKEN {{ KNOWI_CUSTOMER_TOKEN }}
ENV OKTA_AUTH_TOKEN {{ OKTA_AUTH_TOKEN }}
CMD ["python", "app.py"]
