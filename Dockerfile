# Используем официальный образ Python в качестве базового
# FROM python:3.11
FROM ubuntu:latest

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /dashboard

# Копируем все файлы проекта в рабочую директорию
COPY . /dashboard

# Устанавливаем зависимости
RUN apt update && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update
RUN apt upgrade -y
# RUN apt install python3.11 python3-pip -y
RUN apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
RUN python3.11 -m venv .venv
RUN .venv/bin/python -m pip install --no-cache-dir -r requirements_dash.txt
# RUN python3 -m pip install --no-cache-dir -r requirements_dash.txt

# Открываем порт для доступа к приложению
EXPOSE 8050

# WORKDIR /dash

# Запускаем приложение
# CMD ["sh", "-c", "ip -br a && cd dash && python3.11 app.py"]
# CMD ["sh", "-c", "source venv/Scripts/activate && cd dash && python app.py"]
WORKDIR /dashboard/dash
# CMD ['$pwd/.venv/bin/python', 'app.py']
CMD ["/dashboard/.venv/bin/python", "app.py"]
