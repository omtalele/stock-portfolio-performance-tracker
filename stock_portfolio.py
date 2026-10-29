import csv
import os
from datetime import datetime

CSV_FILE = "portfolio_log.csv"


def get_positive_number(message, allow_zero=False):
    while True:
        try:
            value = float(input(message))
            if value > 0 or (allow_zero and value == 0):
                return value
            print("Please enter a valid positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def track_portfolio():
    portfolio = []
    print("\n=== Stock Portfolio Performance Tracker ===")

    while True:
        ticker = input("\nEnter stock ticker (e.g. TCS): ").strip().upper()

        if not ticker:
            print("Ticker cannot be empty.")
            continue

        buy_price = get_positive_number("Enter buy price: ")
        quantity = get_positive_number("Enter share quantity: ")
        current_price = get_positive_number("Enter current price: ", True)

        investment = buy_price * quantity
        current_value = current_price * quantity
        gain_loss = current_value - investment
        percentage = (gain_loss / investment) * 100

        portfolio.append({
            "ticker": ticker,
            "buy_price": buy_price,
            "quantity": quantity,
            "current_price": current_price,
            "investment": investment,
            "current_value": current_value,
            "gain_loss": gain_loss,
            "percentage": percentage
        })

        more = input("Add another stock? (yes/no): ").strip().lower()
        if more not in ("yes", "y"):
            break

    total_investment = sum(s["investment"] for s in portfolio)
    total_value = sum(s["current_value"] for s in portfolio)
    total_gain_loss = total_value - total_investment
    total_percentage = (
        total_gain_loss / total_investment * 100
        if total_investment else 0
    )

    print("\n========== PORTFOLIO SUMMARY ==========")
    print(f"{'Stock':<10}{'Investment':>13}{'Current Value':>16}"
          f"{'Gain/Loss':>13}{'Gain/Loss %':>14}")

    for stock in portfolio:
        print(
            f"{stock['ticker']:<10}"
            f"{stock['investment']:>13.2f}"
            f"{stock['current_value']:>16.2f}"
            f"{stock['gain_loss']:>13.2f}"
            f"{stock['percentage']:>13.2f}%"
        )

    print("-" * 66)
    print(f"Total Investment: Rs. {total_investment:.2f}")
    print(f"Current Value:    Rs. {total_value:.2f}")
    print(f"Total Gain/Loss:  Rs. {total_gain_loss:.2f}")
    print(f"Gain/Loss:        {total_percentage:.2f}%")

    file_exists = os.path.exists(CSV_FILE)
    fieldnames = [
        "date", "ticker", "buy_price", "quantity",
        "current_price", "investment", "current_value",
        "gain_loss", "percentage"
    ]

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writeheader()

        for stock in portfolio:
            writer.writerow({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **stock
            })

    print(f"\nPortfolio saved to {CSV_FILE}")


if __name__ == "__main__":
    track_portfolio()
