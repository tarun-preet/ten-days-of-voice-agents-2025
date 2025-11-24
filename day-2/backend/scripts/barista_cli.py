#!/usr/bin/env python3
"""Interactive Barista CLI for Everbean Coffee.
Asks clarifying questions until the order is complete, then saves to `orders/`.
"""
from datetime import datetime
import json
import os
import sys

ORDER_SCHEMA = ["drinkType", "size", "milk", "extras", "name"]

PROMPTS = {
    "drinkType": "What would you like to drink? (e.g. latte, cappuccino, americano)",
    "size": "What size? (small/medium/large)",
    "milk": "Which milk? (dairy/oat/almond/soy)",
    "extras": "Any extras? (comma-separated, or 'none')",
    "name": "What's the name for the order?",
}


def ask(prompt):
    try:
        return input(prompt + " \n> ")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        sys.exit(0)


def normalize_extras(text):
    if not text:
        return []
    t = text.strip()
    if t.lower() == "none":
        return []
    return [e.strip() for e in t.split(",") if e.strip()]


def save_order(order):
    cwd = os.getcwd()
    orders_dir = os.path.join(cwd, "orders")
    os.makedirs(orders_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    name_part = order.get("name") or "guest"
    filename = f"order_{ts}_{name_part.replace(' ', '_')}.json"
    filepath = os.path.join(orders_dir, filename)
    order_copy = {**order, "saved_at": datetime.utcnow().isoformat() + "Z"}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(order_copy, f, indent=2, ensure_ascii=False)
    return filepath


def run():
    print("Welcome to Everbean Coffee — I'm your friendly barista! (type 'quit' to exit)")
    order = {"drinkType": "", "size": "", "milk": "", "extras": [], "name": ""}

    # Loop until all fields filled
    while True:
        for field in ORDER_SCHEMA:
            if field == "extras":
                current = ", ".join(order["extras"]) if order["extras"] else "(none)"
            else:
                current = order.get(field) or ""
            if current:
                continue
            ans = ask(PROMPTS[field])
            if not ans:
                # ask again
                print("Sorry, I didn't catch that.")
                continue
            if ans.strip().lower() in ("quit", "exit"):
                print("Bye — see you next time!")
                return
            if field == "extras":
                order["extras"] = normalize_extras(ans)
            else:
                order[field] = ans.strip()
        # All fields filled — confirm with user
        print("\nGreat — here's your order summary:")
        print(f"  Drink: {order['drinkType']}")
        print(f"  Size: {order['size']}")
        print(f"  Milk: {order['milk']}")
        print(f"  Extras: {', '.join(order['extras']) if order['extras'] else 'none'}")
        print(f"  Name: {order['name']}")
        confirm = ask("Would you like to place this order? (yes/no)")
        if confirm.strip().lower() in ("y", "yes"):
            path = save_order(order)
            print(f"Thanks! Your order was saved to: {path}")
            print("Have a lovely day — enjoy your coffee!")
            return
        else:
            change = ask("Which field would you like to change? (drinkType/size/milk/extras/name) or 'restart'")
            if change.strip().lower() == "restart":
                order = {"drinkType": "", "size": "", "milk": "", "extras": [], "name": ""}
                continue
            if change.strip() in ORDER_SCHEMA:
                field = change.strip()
                # clear that field and continue loop
                order[field] = "" if field != "extras" else []
                continue
            else:
                print("I didn't understand. Restarting confirmation.")
                continue


if __name__ == '__main__':
    run()
