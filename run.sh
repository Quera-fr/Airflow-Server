docker build -t airflow-server .

docker run -p 8060:8080 \
 -v "$(pwd):/opt/airflow" \
 -it airflow-server