
from datetime import datetime

# Каталог товарів та їх залишки на складі
products = {
    1: {"name": "Мишка", "price": 350.50, "stock": 10},
    2: {"name": "Клавіатура", "price": 750.00, "stock": 8},
    3: {"name": "Навушники", "price": 1200.99, "stock": 5},
    4: {"name": "Монітор", "price": 4500.00, "stock": 3},
    5: {"name": "Флешка", "price": 250.25, "stock": 15}
}

# Кошик: ID товару -> кількість
cart = {}

# Дані адміністратора
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin123"

# Лямбда-функції
format_price = lambda price: f"{price:.2f} грн"
calculate_total = lambda items: sum(
    products[item_id]["price"] * quantity
    for item_id, quantity in items.items()
)


def show_catalog():
    print("\n========== КАТАЛОГ ТОВАРІВ ==========")
    print(f"{'ID':<5}{'Назва':<20}{'Ціна':<18}{'В наявності'}")
    print("-" * 55)

    for item_id, item in products.items():
        print(
            f"{item_id:<5}{item['name']:<20}"
            f"{format_price(item['price']):<18}{item['stock']}"
        )


def show_cart():
    print("\n========== ВАШ КОШИК ==========")

    if not cart:
        print("Кошик порожній.")
        return

    for item_id, quantity in cart.items():
        item = products[item_id]
        total = item["price"] * quantity

        print(
            f"{item['name']} | Кількість: {quantity} | "
            f"Ціна: {format_price(item['price'])} | "
            f"Сума: {format_price(total)}"
        )

    print("-" * 40)
    print("Разом:", format_price(calculate_total(cart)))


def add_to_cart():
    show_catalog()

    try:
        item_id = int(input("\nВведіть ID товару: "))
        quantity = int(input("Введіть кількість: "))

        if item_id not in products:
            print("Помилка: такого товару немає.")
            return

        if quantity <= 0:
            print("Кількість повинна бути більшою за 0.")
            return

        available = products[item_id]["stock"] - cart.get(item_id, 0)

        if quantity > available:
            print(f"Недостатньо товару. Доступно для додавання: {available}.")
            return

        cart[item_id] = cart.get(item_id, 0) + quantity
        print("Товар успішно додано до кошика!")

    except ValueError:
        print("Помилка: введіть ціле число.")


def remove_from_cart():
    show_cart()

    if not cart:
        return

    try:
        item_id = int(input("\nВведіть ID товару для видалення: "))

        if item_id not in cart:
            print("Цього товару немає у кошику.")
            return

        quantity = int(
            input("Введіть кількість для видалення (0 — весь товар): ")
        )

        if quantity < 0:
            print("Кількість не може бути від'ємною.")
            return

        if quantity == 0 or quantity >= cart[item_id]:
            del cart[item_id]
            print("Товар повністю видалено з кошика.")
        else:
            cart[item_id] -= quantity
            print("Кількість товару зменшено.")

    except ValueError:
        print("Помилка: введіть ціле число.")


def buy_products():
    show_cart()

    if not cart:
        return

    confirm = input("\nПідтвердити покупку? (так/ні): ").strip().lower()

    if confirm not in ("так", "т", "yes", "y"):
        print("Покупку скасовано.")
        return

    # Повторна перевірка залишків перед покупкою
    for item_id, quantity in cart.items():
        if quantity > products[item_id]["stock"]:
            print("Помилка: недостатньо товару на складі.")
            return

    total = calculate_total(cart)

    for item_id, quantity in cart.items():
        products[item_id]["stock"] -= quantity

    print("\n========== ПОКУПКУ ЗАВЕРШЕНО ==========")
    print("Дата покупки:", datetime.now().strftime("%d.%m.%Y %H:%M"))
    print("Сума покупки:", format_price(total))
    print("Дякуємо за покупку!")

    cart.clear()


def admin_panel():
    print("\n========== ВХІД АДМІНІСТРАТОРА ==========")

    login = input("Логін: ")
    password = input("Пароль: ")

    if login != ADMIN_LOGIN or password != ADMIN_PASSWORD:
        print("Неправильний логін або пароль!")
        return

    print("\nВхід адміністратора успішний!")
    print("\n========== ЗАЛИШКИ НА СКЛАДІ ==========")

    total_stock = 0
    total_value = 0

    for item in products.values():
        print(
            f"{item['name']}: {item['stock']} шт. | "
            f"Ціна: {format_price(item['price'])}"
        )
        total_stock += item["stock"]
        total_value += item["stock"] * item["price"]

    print("-" * 45)
    print("Усього товарів на складі:", total_stock)
    print("Вартість усіх залишків:", format_price(total_value))


def main():
    while True:
        print("\n========== МІНІ МАГАЗИН ==========")
        print("1. Переглянути каталог")
        print("2. Додати товар у кошик")
        print("3. Переглянути кошик")
        print("4. Видалити товар із кошика")
        print("5. Купити товари з кошика")
        print("6. Увійти як адміністратор")
        print("0. Вихід")

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            show_catalog()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            show_cart()
        elif choice == "4":
            remove_from_cart()
        elif choice == "5":
            buy_products()
        elif choice == "6":
            admin_panel()
        elif choice == "0":
            print("Дякуємо за використання магазину!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
