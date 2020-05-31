# For more information, please refer to https://aka.ms/vscode-docker-python
FROM tensorflow/tensorflow:1.7.0-py3 as base

EXPOSE 5000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y git libfontconfig1 libxrender1 libsm6 libxext6 apt-utils
RUN apt-get clean

RUN pip --version
RUN pip install --upgrade pip

COPY docker/requirements.txt /server-requirements.txt
RUN pip install -r /server-requirements.txt

RUN mkdir /root/pretrained_models
COPY docker/download.py /root/pretrained_models/
COPY docker/download_vggace2.py /root/pretrained_models/
WORKDIR /root/pretrained_models
RUN python download.py
RUN python download_vggace2.py
RUN ls -l

COPY ./src/ /workspace
WORKDIR /workspace/

ENV FLASK_APP=server/server.py
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
ENV FLASK_ENV=development
RUN pip install -U --pre ptvsd

#CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0 -p 5000
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m flask run -h 0.0.0 -p 5000
###########START NEW IMAGE: PRODUCTION ###################
FROM base as prod

CMD flask run -h 0.0.0 -p 5000