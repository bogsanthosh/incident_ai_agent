import os
from databricks import sql


def fetch_logs_from_databricks(service_name: str, limit: int = 50):
    with sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT log_message
                FROM incident_demo.incident_logs
                WHERE service_name = ?
                ORDER BY event_time DESC
                LIMIT ?
                """,
                (service_name, limit),
            )
            rows = cursor.fetchall()

    return [row[0] for row in rows]