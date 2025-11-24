#!/usr/bin/env python3
"""Simulate a multi-turn barista conversation and save the order.
This script mirrors the assistant's expected behavior and writes the order
into the `orders/` directory using the same schema.
"""
import json
import os
from datetime import datetime

# Simulated user responses (change these if you want different outputs)
responses = {
    "drinkType": "cappuccino",
    "size": "large",
    "milk": "almond",
    "extras": "caramel, extra shot",  # comma-separated
    "name": "Jordan",
}

# Simulate the conversation (printed to stdout)
print("Everbean Barista: Hi! Welcome to Everbean Coffee. What would you like to order?")
print(f"User: {responses['drinkType']}")
print("Everbean Barista: What size would you like (small/medium/large)?")
print(f"User: {responses['size']}")
print("Everbean Barista: What milk would you like (dairy/oat/almond/soy)?")
print(f"User: {responses['milk']}")
print("Everbean Barista: Any extras (say 'none' or list comma-separated extras)?")
print(f"User: {responses['extras']}")
print("Everbean Barista: Who should I put the order in the name of?")
print(f"User: {responses['name']}")

# Build order object
extras_list = [e.strip() for e in responses['extras'].split(',') if e.strip()] if responses['extras'].strip().lower() != 'none' else []
order = {
    "drinkType": responses['drinkType'],
    "size": responses['size'],
    "milk": responses['milk'],
    "extras": extras_list,
    "name": responses['name'],
}

# Save to orders/ directory (create it if it doesn't exist)
cwd = os.getcwd()
orders_dir = os.path.join(cwd, 'orders')
os.makedirs(orders_dir, exist_ok=True)
ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
filename = f"order_{ts}_{order.get('name','guest').replace(' ','_')}.json"
filepath = os.path.join(orders_dir, filename)
order_copy = {**order, 'saved_at': datetime.utcnow().isoformat() + 'Z'}
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(order_copy, f, indent=2, ensure_ascii=False)

print('\nEverbean Barista: Thanks! Your order is placed. Summary:')
print(json.dumps(order_copy, indent=2, ensure_ascii=False))
print(f"\nOrder saved to: {filepath}")
