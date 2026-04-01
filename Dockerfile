FROM jupyter/scipy-notebook:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
