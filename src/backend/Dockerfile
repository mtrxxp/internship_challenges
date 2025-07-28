FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt из подкаталога
COPY youtube_scrapper_for_internship_main/requirements.txt ./requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь backend (включая подкаталоги)
COPY . .

# Запуск команды указывается в docker-compose.yml