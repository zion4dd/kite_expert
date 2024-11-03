FROM python:3.12

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
COPY ./kite_expert /app
RUN chmod 777 /app

WORKDIR /app/
# RUN mkdir log
# RUN touch log/debug.log
# RUN chmod 777 log
# RUN chmod 777 log/debug.log
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["/start.sh"]
