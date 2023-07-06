# Workshop по Docker

## Демонстрация

### Сборка простого образа

В папке [simple_dockerfile](./simple_dockerfile):
```
docker build . -t simple_app
docker run --rm simple_app
docker images 
docker rmi
```

### docker-compose

В папке [simple_docker_compose](./simple_docker_compose):

```
python -c "from random import choice; print('SECURE_PASSWORD=' + ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%^*(-_)') for i in range(10)]))"  > .env
cd visualisation
docker build . -t visualisation
cd ../
docker compose build
docker compose up -d
docker compose logs --tail=10 -f
```

# exchangerate-etl-example

Для запуска выполнить следующие команды:
```bash
docker-compose up airflow-init
```
```bash
docker-compose up -d
```
```bash
docker-compose run airflow-cli airflow variables set pg_ip $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=exchangerate-etl-example_db_1"))
```
```bash
docker-compose run airflow-cli airflow dags unpause exchange_rate
```

UI Airflow доступен по адресу http://localhost:8080/
DAG называется exchange_rate. Проверить успешность выполнения можно по наличию записи 'Run successfully' в логе.

Данные можно посмотреть в таблице rates запросом:
```sql
select * from rates
```

Для остановки и удаления образов выполнить команду:
```bash
docker-compose down --volumes --rmi all
```
