FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y curl software-properties-common \
    && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get install -y python3.9 python3.9-dev\
    && apt-get install -y python3-pip

RUN groupadd appuser
RUN useradd -rm -d /home/appuser -s /bin/bash -g root -G sudo,appuser -u 1001 appuser
RUN chown -R appuser /home/appuser
USER appuser
WORKDIR /home/appuser/app

COPY --chown=appuser . .
RUN echo 'alias pip3.9="python3.9 -m pip"' >> ~/.bashrc
RUN python3.9 -m pip install -r requirements.txt


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python3.9", "app.py"]

EXPOSE 5000

