FROM python:3.10.6
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --user pyTelegramBotAPI
RUN pip install --user aiohttp
CMD ["python", "bot.py"]