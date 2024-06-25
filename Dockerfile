# Используем официальный образ Python в качестве базового
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /dashboard

# Копируем все файлы проекта в рабочую директорию
COPY . /dashboard

# Устанавливаем зависимости
RUN python3.11 -m pip install --no-cache-dir -r requirements_dash.txt
# RUN 

# Открываем порт для доступа к приложению
EXPOSE 8050

# WORKDIR /dash

# Запускаем приложение
CMD ["sh", "-c", "ip -br a && cd dash && python3.11 app.py"]
# CMD ["sh", "-c", "source venv/Scripts/activate && cd dash && python app.py"]

