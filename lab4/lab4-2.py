import pickle
from bst import BinarySearchTree

BACKUP_FILE = 'bst_backup.pickle'


def load_tree():
    try:
        with open(BACKUP_FILE, 'rb') as f:
            data = pickle.load(f)
            tree = BinarySearchTree()
            tree.root = tree.deserialize(data)
            return tree
    except (FileNotFoundError, pickle.PickleError):
        return BinarySearchTree()


def save_tree(tree):
    with open(BACKUP_FILE, 'wb') as f:
        pickle.dump(tree.serialize(), f)


def main():
    tree = load_tree()

    while True:
        command = input("Введите команду (add X, find X, delete X, print, clear, dump, exit): ").strip().split()
        if not command:
            continue

        if command[0] == 'add':
            if len(command) != 2:
                print("Неверный формат команды. Используйте: add X")
                continue
            tree.insert(int(command[1]))
            print(f"Элемент {command[1]} добавлен в дерево.")

        elif command[0] == 'find':
            if len(command) != 2:
                print("Неверный формат команды. Используйте: find X")
                continue
            if tree.find(int(command[1])):
                print(f"Элемент {command[1]} найден в дереве.")
            else:
                print(f"Элемент {command[1]} не найден в дереве.")

        elif command[0] == 'delete':
            if len(command) != 2:
                print("Неверный формат команды. Используйте: delete X")
                continue
            tree.delete(int(command[1]))
            print(f"Элемент {command[1]} удален из дерева.")

        elif command[0] == 'print':
            print("Элементы дерева в отсортированном порядке:")
            tree.print_tree()
            print()

        elif command[0] == 'clear':
            tree.clear()
            print("Дерево очищено.")

        elif command[0] == 'dump':
            save_tree(tree)
            print("Резервная копия дерева создана.")

        elif command[0] == 'exit':
            break

        else:
            print("Неизвестная команда. Попробуйте еще раз.")


if __name__ == "__main__":
    main()