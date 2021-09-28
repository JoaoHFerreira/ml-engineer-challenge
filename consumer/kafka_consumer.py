from kafka import KafkaConsumer
from kafka_repository import KafkaTopicsRepository
from psycopg2 import errors
import os
import json
import time


class ConsumerServer(KafkaConsumer):
    def __init__(self):
        self.consumer = self._get_consumer()

    def consume(self):
        while True:
            for metadata, consumer_record in self.consumer.poll().items():
                self._store_values(metadata, consumer_record)
                time.sleep(0.2)

    def _get_consumer(self):
        consumer = KafkaConsumer(
            bootstrap_servers="a49784be7f36511e9a6b60a341003dc2-1378330561.us-east-1.elb.amazonaws.com:9092",
            request_timeout_ms=40000,
            auto_offset_reset="earliest",
            max_poll_records=1000,
        )

        consumer.subscribe(topics=list(consumer.topics()))
        return consumer

    def _store_values(self, metadata, consumer_record):
        kafka_topics_repo = KafkaTopicsRepository()
        consumer_record = self._decode_bin_json_list(consumer_record)
        table_name = metadata.topic.replace("-", "_")
        try:
            with kafka_topics_repo.connect() as kafka_conn:
                kafka_topics_repo.insert_topic_messages_in_batch(
                    conn=kafka_conn,
                    table_name=table_name,
                    consumer_record=consumer_record,
                )
        except Exception as error:

            if errors.UndefinedTable == type(error):
                kafka_topics_repo.create_table_if_not_exists(
                    kafka_conn, metadata, consumer_record
                )
                self._store_values(metadata, consumer_record)
                return

            if errors.UndefinedColumn == type(error):
                column = str(error).split(" ")[1].replace('"', "")
                kafka_topics_repo.create_column_if_not_exists(
                    kafka_conn, metadata, column
                )
                self._store_values(metadata, consumer_record)
                return

    @staticmethod
    def _decode_bin_json_list(bin_json_list):
        if isinstance(bin_json_list[0], dict):
            return bin_json_list

        return list(
            map(
                lambda bin_json_value: json.loads(bin_json_value.value.decode()),
                bin_json_list,
            )
        )


if __name__ == "__main__":
    ConsumerServer().consume()
