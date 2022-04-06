FROM python:3.8.0

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y python3-opencv

COPY BlazeFace-TFLite-Inference ./BlazeFace-TFLite-Inference/

WORKDIR "./BlazeFace-TFLite-Inference"

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "./imageFaceDetection.py" ]

