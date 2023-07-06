from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.python_operator import PythonOperator


def api_call():
    from airflow.models import Variable
    import requests
    import psycopg2

    url = 'https://api.exchangerate.host/latest?base=BTC&symbols=USD&source=crypto'
    response = requests.get(url)
    data = response.json()

    conn = psycopg2.connect(database="postgres", user='postgres', password='postgres', host=Variable.get("pg_ip"), port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO rates(pair, date, rate, timestamp) VALUES ('BTC/USD', {data['date']}, {data['rates']['USD']}, current_timestamp)''')
    conn.close()

    print('Run successfully')
    

with DAG(
    'exchange_rate',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='A simple tutorial DAG',
    schedule_interval='0 */3 * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example']
) as dag:
    t0 = PythonOperator(task_id='get_rate', python_callable=api_call)
