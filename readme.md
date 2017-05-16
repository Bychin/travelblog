# travelblog

## last update:
- добавлена поддержка Centrifugo для лайков и комментариев к постам

## previous updates:
- добавлены карты к постам
- добавлены картинки к постам
- добавлены лайки и комментарии
- исправления багов

## how to configure:
./configure

## how to run
- start [Centrifugo](https://github.com/centrifugal/centrifugo/releases/) with command:
./centrifugo --port 9000 --insecure_api --insecure
- ./run.sh
    or
python3.6 (or python3 if associated with 3.6) manage.py runserver
