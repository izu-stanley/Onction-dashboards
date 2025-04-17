FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /

ENV PATH="/root/.local/bin:$PATH"
COPY . .
RUN pip install -r requirements.txt
RUN cd app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
