# Задаём базовый образ - в данном случае ос - alpine linux с предустановленным python 3.8
FROM python:3.8-buster
# Создаём внутри образа директорию /code и делаем её рабочей (т.е. перемещаемся туда)
WORKDIR /code
# Задаём необходимые переменные среды
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
# Копируем в образ необходимые файлы приложения
COPY requirements.txt requirements.txt
COPY app.py app.py
# Устанавливаем зависимости
RUN apt update && apt install gcc
RUN pip install -r requirements.txt
# Открываем доступ через порт 5000 (который был установлен выше с помощью переменной среды)
EXPOSE 5000
# Задаём команду, которая должна быть выполнена при активации контейнера. В данном случае запускается сервер flask.
CMD ["flask", "run"]