from colorama import Fore, Style
from pathlib import Path
import sys

def show_directory_tree(start_path, root, indent=''):
    path = Path(start_path)

    if not path.exists():
        print(f'Шлях {path} не існує')
        return

    if start_path == root:
        print(f'📦 {path.name}')
        indent = '  '

    for item in path.iterdir():
        if item.is_dir():
            print(Fore.BLUE + f'{indent}📁 {item.name}')
            show_directory_tree(item, root, indent + '  ')
        else:
            print(Fore.GREEN + f'{indent}📜 {item.name}')

def main():
    if len(sys.argv) < 2:
        print("Будь ласка, вкажіть шлях до директорії.")
        return

    root = sys.argv[1]
    show_directory_tree(root, root)

if __name__ == "__main__":
    main()
