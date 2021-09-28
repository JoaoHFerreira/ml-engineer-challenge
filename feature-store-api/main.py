from fastapi import FastAPI
from api_repository import Tables, Columns, Query
from api_documentation import tags_metadata

app = FastAPI(
    title="Feature Store API",
    description="""This API aim to serve on demand analysis of Ifood features.
    \n Choose your table;
    \n Choose your column;
    \n Make your own aggregations""",
    openapi_tags=tags_metadata,
)


@app.get("/tables/", tags=["tables"])
async def get_available_tables():
    return Tables().get_tables()


@app.get("/columns-of-table/{table}", tags=["columns-of-table"])
async def get_available_columns(table):
    return Columns().get_columns(table)


@app.get("/query/{query}", tags=["query"])
async def get_query(query):
    print(query)
    return Query().get_query(query)
