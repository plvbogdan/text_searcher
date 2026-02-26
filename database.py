import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import textract
import tempfile
import io
from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    return SessionLocal()

class FileIndex(Base):
    __tablename__ = "file_index"
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String, unique=True)
    container_path = Column(String) 
    extension = Column(String)
    content_text = Column(Text)     
    file_size = Column(Integer)    
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)

def save_document(file_name, file_path, container, file_bytes, ext):
    db = get_db()

    text = ""
    try:
        if ext == '.txt':
            text = file_bytes.decode('utf-8')
        else:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
                f.write(file_bytes)
                tmp = f.name
            
            text = textract.process(tmp).decode('utf-8')
            os.unlink(tmp) 
            
        print(f"{file_name}: {len(text)} символов")
    except Exception as e:
        print(f"{file_name}: {e}")

    existing = db.query(FileIndex).filter_by(file_path=file_path).first()

    if existing:
        existing.content_text = text
        existing.file_size = len(file_bytes)
        print(f'Обновлён: {file_name}')
    else:
        doc = FileIndex(
            file_name=file_name,
            file_path=file_path,
            container_path=container,
            extension=ext,
            content_text=text,
            file_size=len(file_bytes)
        )
        db.add(doc)
        print(f'Добавлен: {file_name}')
        
    db.commit()
    db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print('Таблица создана')