import psycopg2
import os


class KafkaTopicsRepository:
    def __init__(self):
        self.postgres_host = os.getenv("POSTGRES_HOST")
        self.postgres_dbname = os.getenv("POSTGRES_DBNAME")
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")

    def connect(
        self,
    ):
        with psycopg2.connect(self._get_conn_credentials()) as conn:
            return conn

    def _get_conn_credentials(self):
        return "host={} dbname={} user={} password={}".format(
            self.postgres_host,
            self.postgres_dbname,
            self.postgres_user,
            self.postgres_password,
        )

    def insert_topic_messages_in_batch(self, conn, table_name, consumer_record):
        with conn.cursor() as cursor:
            cursor.execute(
                self._topic_messages_sql_template(table_name, consumer_record)
            )
            conn.commit()

    def create_table_if_not_exists(self, conn, metadata, consumer_record):
        table_name = metadata.topic.replace("-", "_")
        data_sample = consumer_record[0]
        with conn.cursor() as cur:
            cur.execute(self._create_table_sql(table_name, data_sample))
            conn.commit()

    def create_column_if_not_exists(self, conn, metadata, column):
        table_name = metadata.topic.replace("-", "_")

        with conn.cursor() as cur:
            cur.execute(self._create_column_sql(table_name, column))
            conn.commit()

    def _create_column_sql(self, table_name, column):
        return (
            "ALTER TABLE " + table_name + " ADD COLUMN " + column + " text DEFAULT NULL"
        )

    def _create_table_sql(self, table_name, data_sample):
        create_table = (
            "CREATE TABLE {}(\n".format(table_name)
            + " text DEFAULT NULL,\n".join([key for key in data_sample])
            + " text DEFAULT NULL);"
        )
        return create_table

    def _topic_messages_sql_template(self, table_name, consumer_record):
        return "\n".join(
            list(
                map(lambda row: self._prepare_insert(table_name, row), consumer_record)
            )
        )

    @staticmethod
    def _prepare_insert(table_name, row):
        insert_header = "INSERT INTO {}(".format(table_name)
        columns_to_insert = ", ".join([key for key, _ in row.items()]) + ")"
        values_to_insert = " VALUES ({})".format(
            ", ".join(["'" + str(value) + "'" for _, value in row.items()])
        )
        return insert_header + columns_to_insert + values_to_insert + ";"
