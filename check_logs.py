from sqlalchemy import text
from database.db import engine

with engine.connect() as connection:

    deployments = connection.execute(
        text("SELECT * FROM deployments")
    )

    print("\nDEPLOYMENTS\n")

    for row in deployments:
        print(row)

    validations = connection.execute(
        text("SELECT * FROM validations")
    )

    print("\nVALIDATIONS\n")

    for row in validations:
        print(row)
