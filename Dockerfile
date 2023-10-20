FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir discord.py==1.7.3
RUN pip install --no-cache-dir python-a2s==1.3.0

COPY . .

CMD ["python", "./main.py"]