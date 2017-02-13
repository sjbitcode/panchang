FROM python:3.6-alpine

ENV INSTALL_PATH /worker
RUN mkdir -p $INSTALL_PATH $INSTALL_PATH/log

WORKDIR $INSTALL_PATH

COPY ./requirements.txt $INSTALL_PATH
RUN pip install -r requirements.txt

COPY . $INSTALL_PATH
