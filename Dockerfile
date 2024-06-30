# Используем официальный образ Python
FROM python

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg

# Копируем все файлы приложения
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "bot.py"]