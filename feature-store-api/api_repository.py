import psycopg2
import os


class Utils:
    def _get_postgres_conn(self):
        with psycopg2.connect(
            f"""host={os.getenv("POSTGRES_HOST")} dbname={os.getenv("POSTGRES_DBNAME")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")}"""
        ) as conn:
            return conn

    def _list_of_tuple_to_list_of_dict(self, element_name, cur):
        return [
            {f"{element_name}_{num}": element[0]}
            for num, element in enumerate(cur.fetchall())
        ]


class Tables(Utils):
    def get_tables(self):
        element_name = "table_name"
        with self._get_postgres_conn().cursor() as cur:
            cur.execute(self._get_tables_sql_template())
            return self._list_of_tuple_to_list_of_dict(element_name, cur)

    @staticmethod
    def _get_tables_sql_template():
        return """
        SELECT 
            table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
        """


class Columns(Utils):
    def get_columns(self, table_name):
        element_name = "column_name"
        with self._get_postgres_conn().cursor() as cur:
            cur.execute(self._get_columns_sql_template(table_name))
            return self._list_of_tuple_to_list_of_dict(element_name, cur)
            # return [
            #     {f"column_{num}": column_name[0]}
            #     for num, column_name in enumerate(cur.fetchall())
            # ]

    @staticmethod
    def _get_columns_sql_template(table_name):
        return f"""
            SELECT
                column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name   = '{table_name}'
        """


class Query(Utils):
    def get_query(self, query):
        query_result = "query_result"
        with self._get_postgres_conn().cursor() as cur:
            cur.execute(query)
            return {query_result: [element for element in cur.fetchall()]}
