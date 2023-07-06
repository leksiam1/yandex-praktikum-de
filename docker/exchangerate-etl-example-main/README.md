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
