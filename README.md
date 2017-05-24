# travelblog

### RС v0.9.5

### last update:
- улучшена графическая оболочка
- добавлен поиск по городу при создании поста
- исправления багов и оптимизация кода


### previous updates:
- добавлена полная поддержка [Centrifugo](https://github.com/centrifugal/centrifugo/releases/) для лайков к постам
- добавлены карты к постам
- добавлены картинки к постам
- добавлены лайки и комментарии


## How to configure:
./configure

## How to run:
- Start [Centrifugo](https://github.com/centrifugal/centrifugo/releases/) with command:
```
./centrifugo --port 9000 --insecure_api --insecure
```
- Use provided bash script for test and etc...:
```
./run.sh
```
- ... or start blog with this django command:
```
python3.6 (or python3 if associated with 3.6) manage.py runserver
```
