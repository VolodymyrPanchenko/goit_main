import queue
import random

class Request:
  def __init__(self, name):
    self.name = name
    self.operations = random.randint(1, 5)


#Створити чергу заявок
request_queue = queue.Queue()

#Функція generate_request():
def generate_request():
    name = f"Request-{random.randint(1000, 9999)}"
    request = Request(name)
    request_queue.put(request)  
    print(f"Generated: {request.name} with {request.operations} operations")

#Функція process_request():
def process_request():
    if not request_queue.empty():
        request = request_queue.get()
        print(f"Processing: {request.name} with {request.operations} operations")
    else:
        print("Queue is empty")  

# Головний цикл програми
def main():
    while True:
        command = input("\nНатисніть Enter для створення нової заявки або 'exit' для виходу: ").strip().lower()
        if command == "exit":
            print("Програма завершена.")
            break
        
        # Генерація та обробка
        generate_request()
        process_request()

if __name__ == "__main__":
    main()
