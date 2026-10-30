from pathlib import Path

def total_salary(path):
    total = 0
    count = 0
    try:
        with open(path, "r") as fh:
            rows = [line.strip().split(",") for line in fh]
            for row in rows:
                if len(row) >= 2:
                    try:
                        total += int(row[1])
                        count += 1
                    except ValueError:
                        continue 
        if count > 0:
            average = total // count
        else:
            average = 0
        return total, average
    except FileNotFoundError:
        print(f"File not found: {path}")
    except IOError as e:
        print(f"I/O error: {e}")
    return 0, 0  

total, average = total_salary("emp.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")

def get_cats_info(path):
    cats = []
    try:
        with open(path, "r") as fh:
            rows = [line.strip().split(",") for line in fh]
            for row in rows:
                if len(row) >= 3:
                    try:
                        age = int(row[2])
                        cats.append( {"id": row[0], "name": row[1], "age":age})   
                    except ValueError:
                        continue 
        return cats
    except FileNotFoundError:
        print(f"File not found: {path}")
    except IOError as e:
        print(f"I/O error: {e}")
    return [] 

# cats_info = get_cats_info("cats_info.txt")
# print(cats_info)



