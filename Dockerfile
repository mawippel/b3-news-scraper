FROM python:3.7-slim-buster
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen
RUN pip install -r requirements.txt
EXPOSE 80
CMD python -u ./src/cron_job.py