import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    description = input("Description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid positive amount.")
        return

    category = input("Category: ").strip().title() or "Other"

    expense = {
        "id": len(expenses) + 1,
        "description": description,
        "amount": amount,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully.")


def show_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<5}{'Description':<25}{'Category':<15}{'Amount':>12}{'Date':>15}")
    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"{expense['description'][:24]:<25}"
            f"{expense['category'][:14]:<15}"
            f"${expense['amount']:>11.2f}"
            f"{expense['date']:>15}"
        )

    print("-" * 75)


def show_summary(expenses):
    if not expenses:
        print("\nNo expenses to summarize.")
        return

    total = sum(expense["amount"] for expense in expenses)

    categories = {}

    for expense in expenses:
        category = expense["category"]
        categories[category] = categories.get(category, 0) + expense["amount"]

    print("\nExpense Summary")
    print("-" * 30)
    print(f"Total spent: ${total:.2f}")

    print("\nBy category:")

    for category, amount in sorted(
        categories.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{category:<20} ${amount:.2f}")


def delete_expense(expenses):
    show_expenses(expenses)

    if not expenses:
        return

    try:
        expense_id = int(input("\nEnter the ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print("Expense deleted successfully.")
            return

    print("Expense ID not found.")


def display_menu():
    print("\n" + "=" * 40)
    print("       PERSONAL EXPENSE TRACKER")
    print("=" * 40)
    print("1. Add expense")
    print("2. View expenses")
    print("3. View summary")
    print("4. Delete expense")
    print("5. Exit")
    print("=" * 40)


def main():
    expenses = load_expenses()

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            show_expenses(expenses)

        elif choice == "3":
            show_summary(expenses)

        elif choice == "4":
            delete_expense(expenses)

        elif choice == "5":
            print("Thanks for using Expense Tracker!")
            break

        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
