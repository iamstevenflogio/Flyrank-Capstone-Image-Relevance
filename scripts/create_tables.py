from app.database import Base, engine
from app.models.image import Image, ImageMetadata

def main():
    print("Tables SQLAlchemy knows about:")
    print(list(Base.metadata.tables.keys()))

    Base.metadata.create_all(bind=engine)

    print("Database tables created.")

if __name__ == "__main__":
    main()