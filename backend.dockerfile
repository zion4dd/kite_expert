FROM python:3.12-slim

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./kite_expert /app
RUN chmod 777 /app

WORKDIR /app/

# EXPOSE 8000

CMD ["/start.sh"]
