FROM python:3.11

COPY requirements.txt app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "stout_frontendapp.py", "--server.address=0.0.0.0","--server.port=8501"]