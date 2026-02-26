import os
import zipfile
from pathlib import Path
import io
import py7zr
import rarfile
import tempfile
from database import save_document

def dfs(entry, container=None, level=0):
    indent = " " * level

    if isinstance(entry, (str, Path)):
        entry = Path(entry)

        if entry.is_dir():
            print(f'{indent}Folder: {entry.name}')
            for child in entry.iterdir():
                dfs(child, container, level + 1)
        
        elif entry.is_file():
            ext = entry.suffix.lower()
            print(f'{indent}File: {entry.name}')

            if ext in ['.zip', '.7z', '.rar']:
                archive_process(entry, container, level, source_type='disk')
            else:
                process_document(entry, container, level)

    elif isinstance(entry, tuple) and len(entry) == 2:
        filename, file_bytes = entry
        ext = Path(filename).suffix.lower()

        if ext in ['.zip', '.7z', '.rar']:
            archive_process((filename, file_bytes), container, level, source_type='memory')
        else:
            process_document(entry, container, level)




def archive_process(entry, container, level, source_type):
    if source_type == 'disk':
        ext = Path(entry).suffix.lower()
    else:
        filename, _ = entry
        ext = Path(filename).suffix.lower()
    
    if ext == '.zip':
        zip_archive_process(entry, container, level, source_type)
    elif ext == '.7z':
        sevenz_archive_process(entry, container, level, source_type)
    elif ext == '.rar':
        rar_archive_process(entry, container, level, source_type)
    else:
        print(f"Неподдерживаемый формат архива: {ext}")



def zip_archive_process(entry, container, level, source_type):
    indent = ' ' * level

    if source_type == 'disk':
        path = Path(entry)
        print(f'{indent} ZIP archive: {path.name}')
        zip_file = zipfile.ZipFile(path, 'r')
        base_container = f'{container}/{path.name}' if container else str(path)
    else:
        filename, bytes_data = entry
        print(f'{indent} ZIP archive: {filename}')
        zip_file = zipfile.ZipFile(io.BytesIO(bytes_data), 'r')
        base_container = f'{container}/{filename}'

    with zip_file:
        for file in zip_file.namelist():
            file_bytes = zip_file.read(file)
            dfs((file, file_bytes), base_container, level + 1)

def sevenz_archive_process(entry, container, level, source_type):
    indent = ' ' * level
    if source_type == 'disk':
        path = Path(entry)
        print(f'{indent} 7z archive: {path.name}')
        sz = py7zr.SevenZipFile(path, 'r')
        base_container = f'{container}/{path.name}' if container else str(path)
    else:
        filename, bytes_data = entry
        print(f'{indent} 7z archive: {filename}')
        with tempfile.NamedTemporaryFile(suffix='.7z', delete=False) as tmp:
            tmp.write(bytes_data)
            tmp_path = tmp.name
        sz = py7zr.SevenZipFile(tmp_path, 'r')
        base_container = f'{container}/{filename}'

    with tempfile.TemporaryDirectory() as temp_dir:
        sz.extractall(path=temp_dir)
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
                rel_path = Path(root).relative_to(temp_dir) / file
                dfs((str(rel_path), file_bytes), base_container, level + 1)

    if source_type != 'disk':
        os.unlink(tmp_path)

import patoolib
import logging


logging.getLogger('patool').setLevel(logging.WARNING)

def rar_archive_process(entry, container, level, source_type):
    indent = ' ' * level
    need_cleanup = None

    if source_type == 'disk':
        path = Path(entry)
        print(f'{indent} RAR archive: {path.name}')
        rar_path = str(path)
        base_container = f'{container}/{path.name}' if container else str(path)
    else:
        filename, bytes_data = entry
        print(f'{indent} RAR archive: {filename}')
        with tempfile.NamedTemporaryFile(suffix='.rar', delete=False) as tmp:
            tmp.write(bytes_data)
            rar_path = tmp.name
        base_container = f'{container}/{filename}'
        need_cleanup = rar_path

    with tempfile.TemporaryDirectory() as temp_dir:
        patoolib.extract_archive(rar_path, outdir=temp_dir)
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
                rel_path = Path(root).relative_to(temp_dir) / file
                dfs((str(rel_path), file_bytes), base_container, level + 1)

    if need_cleanup:
        os.unlink(need_cleanup)




def process_document(source, container, level, source_type=None):
    indent = ' ' * level
    
    if source_type is None:
        if isinstance(source, (str, Path)):
            source_type = 'disk'
        else:
            source_type = 'memory'
    
    if source_type == 'disk':
        file_path = source
        file_name = file_path.name
        print(f'{indent} Document: {file_name}')

        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        
        full_path = str(file_path)
        ext = file_path.suffix.lower()
    
    else: 
        filename, file_bytes = source
        file_name = Path(filename).name
        print(f'{indent} Document {filename}')

        full_path = filename
        ext = Path(filename).suffix.lower()
    
    save_document(
        file_name=file_name,
        file_path=full_path,
        container=container,
        file_bytes=file_bytes,
        ext=ext
    )