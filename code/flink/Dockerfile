FROM python:3.9

WORKDIR /App

COPY . .

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install -r flink_requirements.txt

CMD ["python","camera_consumer.py"]

