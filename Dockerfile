FROM python:3.9
WORKDIR /src
COPY ./src /src
RUN pip install --no-cache-dir -r /src/requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
CMD [ "uvicorn","server:app","--host","0.0.0.0","--port","80" ]