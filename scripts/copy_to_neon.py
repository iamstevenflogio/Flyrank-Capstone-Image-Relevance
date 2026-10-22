from getpass import getpass

from sqlalchemy import create_engine, func, select, text

from app.database import Base, engine as local_engine
from app.models.image import Image, ImageMetadata, AICallLog


def main():
    url = getpass("Paste your Neon connection string (hidden): ").strip()

    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    remote_engine = create_engine(url)

    if remote_engine.url.host == local_engine.url.host:
        raise RuntimeError("Source and destination hosts must be different.")

    tables = [
        Image.__table__,
        ImageMetadata.__table__,
        AICallLog.__table__,
    ]

    with local_engine.connect() as source:
        rows_by_table = {
            table.name: [
                dict(row)
                for row in source.execute(select(table)).mappings()
            ]
            for table in tables
        }

    print("\nRecords to copy:")
    for table in tables:
        print(f"{table.name}: {len(rows_by_table[table.name])}")

    print(f"\nDestination host: {remote_engine.url.host}")
    if input("Type COPY to create tables and copy records: ").strip() != "COPY":
        print("Cancelled.")
        return

    with remote_engine.begin() as destination:
        Base.metadata.create_all(destination)

        for table in tables:
            count = destination.scalar(
                select(func.count()).select_from(table)
            )
            if count:
                raise RuntimeError(
                    f"Destination table {table.name} is not empty. "
                    "Stopped without copying records."
                )

        for table in tables:
            rows = rows_by_table[table.name]
            if rows:
                destination.execute(table.insert(), rows)

        for table in tables:
            destination.execute(
                text(
                    "SELECT setval("
                    "pg_get_serial_sequence(:table_name, 'id'), "
                    f'COALESCE((SELECT MAX(id) FROM "{table.name}"), 0) + 1, '
                    "false)"
                ),
                {"table_name": table.name},
            )

    print("\nCopy completed. Local records were not changed.")


if __name__ == "__main__":
    main()