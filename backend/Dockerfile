FROM continuumio/miniconda3:24.1.2-0 AS stout-python-ms

ENV PYTHON_VERSION=3.10

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        openjdk-11-jre \
        curl \
        build-essential \
        gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN conda install -c conda-forge python>=PYTHON_VERSION

RUN python3 -m pip install -U pip

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --upgrade setuptools pip
RUN pip3 install --no-cache-dir -r /code/requirements.txt
RUN pip3 install --no-deps STOUT-pypi>=2.0.5

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "1"]