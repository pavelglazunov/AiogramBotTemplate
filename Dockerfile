FROM python:3.11

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"


EXPOSE 80
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "python3", "bot.py" ]
