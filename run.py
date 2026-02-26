from pathlib import Path
from crawler import dfs
from database import init_db

def main():
    init_db()
    
    scan_path = Path("test_data")
    if scan_path.exists():
        print(f"Сканирование {scan_path}")
        dfs(scan_path)
    else:
        print("Папка test_data не найдена")

if __name__ == "__main__":
    main()