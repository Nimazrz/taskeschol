FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=taskeschol.settings
CMD ["python3", "manage.py",  "runserver", "0.0.0.0:8000"]