import sys
from database import get_db, FileIndex

def highlight_text(text, query):
    words = query.split()
    highlighted = text
    
    for word in words:
        lower_highlighted = highlighted.lower()
        lower_word = word.lower()
        start = 0
        result = []
        
        while True:
            pos = lower_highlighted.find(lower_word, start)
            if pos == -1:
                result.append(highlighted[start:])
                break
            
            result.append(highlighted[start:pos])
            result.append(f"\033[1;31;43m{highlighted[pos:pos+len(word)]}\033[0m")
            start = pos + len(word)
        
        highlighted = ''.join(result)
    
    return highlighted

def search(query):
    db = get_db()
    
    words = query.split()
    
    from sqlalchemy import or_
    
    db_query = db.query(FileIndex)
    
    for word in words:
        db_query = db_query.filter(
            or_(
                FileIndex.content_text.ilike(f'%{word}%'),
                FileIndex.file_name.ilike(f'%{word}%')
            )
        )
    
    results = db_query.all()
    
    print(f"\nНайдено {len(results)} файлов по запросу '{query}':")
    print("=" * 60)
    
    for r in results:
        container = f" [в архиве: {r.container_path}]" if r.container_path else ""
        
        text = r.content_text or ""
        
        first_pos = -1
        for word in words:
            pos = text.lower().find(word.lower())
            if pos != -1 and (first_pos == -1 or pos < first_pos):
                first_pos = pos
        
        if first_pos != -1:
            start = max(0, first_pos - 50)
            end = min(len(text), first_pos + 150)
            context = text[start:end]
            
            if start > 0:
                context = "..." + context
            if end < len(text):
                context = context + "..."
        else:
            context = text[:200] + "..." if len(text) > 200 else text
        
        highlighted = highlight_text(context, query)
        
        print(f"{r.file_name}{container}")
        print(f"   Путь: {r.file_path}")
        print(f"   Текст: {highlighted}")
        print(f"   Размер: {r.file_size} байт")
        print("-" * 40)
        print('\n'*5)
    
    db.close()

if __name__ == "__main__":
    search(sys.argv[1])