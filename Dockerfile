FROM python:3.9
ENV PYTHONUNBUFFERED 1
COPY . /app
WORKDIR app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD source run.sh