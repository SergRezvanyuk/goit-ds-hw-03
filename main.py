from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://rezvaserg:FdhiHDdmAphGFbzg@cluster0.5izpshs.mongodb.net/GoIT8?retryWrites=true&w=majority",
    server_api=ServerApi('1')
)



db = client["cats_database"]
cats_collection = db["cats"]
input('Створено базу даних та колекцію')


def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    cats_collection.insert_one(cat)
    print(f"Кіт {name} успішно доданий.")


def read_all_cats():
    cats = cats_collection.find()
    for cat in cats:
        print(cat)


def read_cat_by_name(name):
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def update_cat_age_by_name(name, new_age):
    result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Вік кота {name} оновлено до {new_age}.")
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def add_feature_to_cat(name, new_feature):
    result = cats_collection.update_one({"name": name}, {"$push": {"features": new_feature}})
    if result.modified_count > 0:
        print(f"Нова характеристика додана до кота {name}.")
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def delete_cat_by_name(name):
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кіт з ім'ям {name} видалений.")
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def delete_all_cats():
    result = cats_collection.delete_many({})
    print(f"Видалено {result.deleted_count} записів.")


if __name__ == "__main__":
    input("Створення записів")
    create_cat("Barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("Murzik", 5, ["любить спати", "білий", "грайливий"])
    
    input("Читання всіх записів")
    print("\nВсі коти:")
    read_all_cats()
    
    input("Читання конкретного кота")
    print("\nКіт по імені Barsik:")
    read_cat_by_name("Barsik")
    
    input("Оновлення віку кота")
    update_cat_age_by_name("Barsik", 4)
    
    input("Додавання характеристики")
    add_feature_to_cat("Barsik", "швидко бігає")
    
    input("Видалення кота Murzik")
    delete_cat_by_name("Murzik")
    
    input("Видалення всіх записів")
    delete_all_cats()
