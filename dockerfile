FROM python:3.10.5

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/menu/
RUN pip install -r requirements.txt
RUN pip install psycopg2
COPY * /app/

WORKDIR /app/menu

EXPOSE 8000
CMD ["python", "menu:manage.py", "runserver", "0.0.0.0:8000"]