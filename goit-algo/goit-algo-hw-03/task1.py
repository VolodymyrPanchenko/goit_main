from pathlib import Path
import shutil
import sys

def copy_files_recursive(source_path: Path, dest_path: Path) -> None:
    """Рекурсивно копіює файли та сортує їх за розширеннями"""
    
    if source_path.is_file():
        # Отримуємо розширення файлу
        extension = source_path.suffix[1:].lower() if source_path.suffix else 'no_extension'
        
        # Створюємо піддиректорію для розширення
        ext_dir = dest_path / extension
        ext_dir.mkdir(exist_ok=True)
        
        try:
            # Копіюємо файл
            shutil.copy2(source_path, ext_dir / source_path.name)
            print(f"Скопійовано: {source_path.name} → {extension}/")
        except Exception as e:
            print(f"Помилка з файлом {source_path.name}: {e}")
    
    elif source_path.is_dir():
        # Рекурсивно обробляємо всі елементи в директорії
        for child in source_path.iterdir():
            copy_files_recursive(child, dest_path)

def main():
    if len(sys.argv) < 2:
        print("Використання: python script.py <source_dir> [dest_dir]")
        sys.exit(1)
    
    source = Path(sys.argv[1])
    dest = Path(sys.argv[2] if len(sys.argv) > 2 else "dist")
    
    if not source.exists():
        print(f"Шлях {source} не існує!")
        sys.exit(1)
    
    # Створюємо директорію призначення
    dest.mkdir(exist_ok=True)
    
    print(f"Копіюємо з {source} до {dest}")
    copy_files_recursive(source, dest)
    print("Готово!")

if __name__ == "__main__":
    main()