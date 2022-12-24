FROM python:3.10.6
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --user telebot
RUN pip install --user asyncio
CMD ["python", "bot.py"]
