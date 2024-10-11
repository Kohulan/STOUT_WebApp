FROM continuumio/miniconda3:24.1.2-0 AS stout-python-ms

ENV PYTHON_VERSION=3.10
ENV RDKIT_VERSION=2023.09.4

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update -y && \
    apt-get install -y openjdk-11-jre && \
    apt-get install -y curl && \
    conda update -n base -c defaults conda

RUN conda install -c conda-forge python>=PYTHON_VERSION

RUN python3 -m pip install -U pip

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --upgrade setuptools pip
RUN pip3 install --no-cache-dir -r /code/requirements.txt
RUN pip3 install --no-deps STOUT-pypi>=2.0.5
RUN python3 -m pip uninstall -y imantics
RUN pip3 install imantics==0.1.12

RUN python3 -m pip install uvicorn[standard]

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "1"]