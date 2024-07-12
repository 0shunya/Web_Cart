import json

users = [
    {
        "id": 1,
        "email": "shloksingh@gmail.com",
        "password": "Discipline123"
    },
    {
        "id": 2,
        "email": "shaneclark123rt@gmail.com",
        "password": "mypassword"
    }
]


products = [
    {
        "Id": 1,
        "Name": "Shoes",
        "Price": 199,
        "Description": "Nike Shoes",
        "Size": "Large",
        "Color": "White",
        "UPI ID": "sjs2805@ybl"
    },
    {
        "Id": 2,
        "Name": "Mat",
        "Price": 200,
        "Description": "Door Mat",
        "Size": "Medium",
        "Color": "Blue",
        "UPI ID": "sjs2805@ybl"
    },
    {
        "Id": 3,
        "Name": "Watch",
        "Price": 300,
        "Description": "Smart Watch",
        "Size": "Small",
        "Color": "Black",
        "UPI ID": "sjs2805@ybl"
    },
    {
        "Id": 4,
        "Name": "Hat",
        "Price": 25,
        "Description": "Pirate Hat",
        "Size": "Big",
        "Color": "Brown",
        "UPI ID": "sjs2805@ybl"
    },
    {
        "Id": 5,
        "Name": "Goggles",
        "Price": 120,
        "Description": "Summer goggles",
        "Size": "Small",
        "Color": "Black",
        "UPI ID": "sjs2805@ybl"
    }
]

carts = [
    {
        "email": "shloksingh@gmail.com",
        "items": [
            {
                "Id": 1,
                "Name": "Shoes",
                "Price": 199,
                "Description": "Nike Shoes",
            }
        ]
    },
    {
        "email": "shaneclark123rt@gmail.com",
        "items": []
    }
]

wishlists = [
    {
        "email": "shloksingh@gmail.com",
        "items": [
            {
                "Id": 2,
                "Name": "Mat",
                "Price": 200,
                "Description": "Door Mat",
            }
        ]
    },
    {
        "email": "shaneclark123rt@gmail.com",
        "items": [
            {
                "Id": 4,
                "Name": "Hat",
                "Price": 25,
                "Description": "Pirate Hat",
            }
        ]
    }
]

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

write_json('users.json', users)
write_json('products.json', products)
write_json('cart.json', carts)
write_json('wishlist.json', wishlists)

print("Data has been written to JSON files.")
