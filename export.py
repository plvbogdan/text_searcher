import csv
import sys
from pathlib import Path
from database import get_db, FileIndex

def export_to_csv(filename="export.csv"):
    
    db = get_db()
    
    results = db.query(FileIndex).all()
    
    if not results:
        print("База данных пуста")
        return
    
    print(f"Найдено записей: {len(results)}")
    
    fields = ['id', 'file_name', 'file_path', 'container_path', 
              'extension', 'content_text', 'file_size', 'created_at']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(fields)
        for row in results:
            writer.writerow([
                row.id,
                row.file_name,
                row.file_path,
                row.container_path or '',
                row.extension or '',
                row.content_text or '',
                row.file_size,
                row.created_at
            ])
    
    print(f"Экспортировано в {filename}")
    print(f"Размер файла: {Path(filename).stat().st_size} байт")
    db.close()

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "export.csv"
    export_to_csv(filename)