from sqlalchemy import create_engine
from sqlalchemy import text

DATABASE_FILE = "patchpilot.db"

engine = create_engine(
    f"sqlite:///{DATABASE_FILE}"
)

def initialize_database():

    with open(
        "database/schema.sql",
        "r"
    ) as file:

        sql_script = file.read()

    with engine.connect() as connection:

        for statement in sql_script.split(";"):

            statement = statement.strip()

            if statement:

                connection.execute(
                    text(statement)
                )

        connection.commit()

    print(
        "Database initialized successfully"
    )
