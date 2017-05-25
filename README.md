# travelblog

### Release v1.0.0

### last update:
- улучшена графическая оболочка
- исправления багов и оптимизация кода
- добавлена функция удаления поста (да, теперь не все, что вы запостите, будет навсегда оставаться на сайте)


### previous updates:
- добавлена полная поддержка [Centrifugo](https://github.com/centrifugal/centrifugo/releases/) для лайков к постам
- добавлен поиск по городу при создании поста



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
