FROM python:3.10
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /app
COPY gateway /app
WORKDIR /app
EXPOSE 8081
ENV PYTHONPATH /app
CMD [ "python", "./gateway/application.py" ]