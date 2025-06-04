from collections import Counter, defaultdict # for Block 4 and Blok 5
import json

##### Block 1: Dictionaries (Theory & Practical Problem) #####
print("\n---Block 1: Dictionaries (Theory & Practical Problem) ---")

# Practical Problem 1.1: Product Inventory Dictionary
# 1. Create a product_inventory dictionary
product_inventory = {
    101: {
        "name": "Laptop",
        "price": 1200.00,
        "stock": 154
    },
    102: {
        "name": "PC",
        "price": 1500.99,
        "stock": 12
    },
    103: {
        "name": "Mouse",
        "price": 39.99,
        "stock": 150
    },
    104: {
        "name": "Keyboard",
        "price": 58.99,
        "stock": 10
    },
    105: {
        "name": "Suitcase",
        "price": 128.99,
        "stock": 4
    },
}

# 2. Demonstrate Dictionary Operations

print(f"The example dictionary: {product_inventory}")
# Print the name and price of a specific product using its ID
print(f"Product's no 102 name: {product_inventory[102]['name']}")
print(f"Product's no 102 price: {product_inventory[102]['price']}")
# Attempt to update the stock of one product
print("Attempt to update the stock of product 102")
print(f"The original amount: {product_inventory[102]['stock']}")
product_inventory[102]["stock"] += 1
print(f"The updated amount: {product_inventory[102]['stock']}")

# Add a brand new product to the inventory.
product_inventory[106] = {
        "name": "Powerbank",
        "price": 25.00,
        "stock": 21
    }
print(f"The updated dictionary: {product_inventory}")

# Remove product with ID 103 from the dictionary
print(f"Remove a product with ID = 103")
del product_inventory[103]
print(f"The dictionary after removing: {product_inventory}")

# Attempt to access a non-existent product ID safely (without causing an error)
result = product_inventory.get(108, "Unknown")
print(f"Access to non-existing product ID: {result}")

# Loop through the product_inventory and print the ID and name of each product.
print("Print the ID and name of each product:")
for key in product_inventory:
    print(f"ID: {key}, "
          f"name: {product_inventory[key]['name']}")

print("-" * 30)


##### Block 2: Tuples & Sets (Theory & Practical Problem) #####
print("\n--- Block 2: Tuples & Sets (Theory & Practical Problem) ---")

### Practical Problem 2.1: Data Analysis with Tuples and Sets

# 1. Tuple Practice
# Create a tuple named rgb_color with 3 integer values representing an RGB color
rgb_color = (255, 0, 128)
print(f"\nThe rgb_color tuple: {rgb_color}")

# Try to change one of tuple's values to confirm its immutability
try:
    print("Attempt to change the third item of the tuple")
    rgb_color[2] = 18
except TypeError as e:
    print(f"Caught an expected exception: {e}")    
except Exception as e:
    print(f"Caught an unexpected exception: {e}")

# Unpack the rgb_color tuple into three separate variables
print(f"Unpacking the rgb_color tuple into variables:")
red, green, blue = rgb_color
print(f"red: {red}, green: {green}, blue: {blue}")

# 2. Set Practice:
# Create a list that contains some duplicate integer IDs
all_student_ids = [101, 105, 103, 101, 107, 103]
print(f"A list to process: {all_student_ids}")

# Converting list into a set
unique_student_ids = set(all_student_ids)
print(f"Converting list into a set: {unique_student_ids}")

# Create another list with some IDs overlapping with all_student_ids
enrolled_in_course_a_ids = [101, 105, 111, 123, 158, 118]
enrolled_in_course_a_ids_set = set(enrolled_in_course_a_ids)

# Demonstrate set operations
print(f"The IDs of students who are in all_student_ids AND enrolled_in_course_a_ids: {unique_student_ids.intersection(enrolled_in_course_a_ids_set)}")
print(f"The IDs of students who are in all_student_ids but NOT enrolled_in_course_a_ids: {unique_student_ids.difference(enrolled_in_course_a_ids_set)}")
print("-" * 30)

##### Block 3: Comprehensions (List & Dictionary) #####
print("\n--- Block 3: Comprehensions (List & Dictionary) ---")

### Practical Problem 3.1: Applying Comprehensions

# 1. List Comprehension: Filtering and Transforming
# Create a list that contain products from product_inventory, whose price is greater than 100.00
high_value_products = [product for product in product_inventory.values() if product["price"] > 100.00]
print(f"A list containing dictionaries for products whose price is greater than 100.00:\n{high_value_products}")

# 2. Dictionary Comprehension: Reorganizing Data
# Create a new dictionary that map each product's id from product_inventory to its name.
product_names_by_id = {product_id: product["name"] for product_id, product in product_inventory.items()}
print(f"Product ID to name: {product_names_by_id}")

# 3. Set Comprehension (Optional Bonus): Extracting Unique Values
# Add new key "category" to the product dictionary
product_inventory_modified = {
    101: {'name': 'Laptop', 'price': 1200.0, 'stock': 154, 'category': 'Electronics'}, 
    102: {'name': 'PC', 'price': 1500.99, 'stock': 13, 'category': 'Electronics'},
    104: {'name': 'Keyboard', 'price': 58.99, 'stock': 10, 'category': 'Accessory'},
    105: {'name': 'Suitcase', 'price': 128.99, 'stock': 4, 'category': 'Case'},
    106: {'name': 'Powerbank', 'price': 25.0, 'stock': 21, 'category': 'Accessory'}
}

print(f"\nA dictionary with added key 'category': {product_inventory_modified}")

# Create set that contains all the distinct categories from product_inventory
unique_categories = {product["category"] for product in product_inventory_modified.values()}
print(f"A set with all the distinct categories from the dictionary: {unique_categories}")
print("-" * 30)

##### Block 4: collections.Counter #####
print("\n--- Block 4: collections.Counter ---")

### Practical Problem 4.1: Analyzing Customer Reviews
# 1.  Create a list of strings representing a customer review.
reviews = [
    "The product is great and fast.",
    "Fast delivery, great service.",
    "Average product, slow delivery.",
    "Great value for money.",
    "Fast response, helpful staff."
]

# 2. Word Frequency Analysis
# Combine all reviews into a single string
reviews_to_string = " ".join(reviews)

# Remove punctuation and convert to lowercase for consistent counting
reviews_to_words = [word.strip(".!?,").lower() for word in reviews_to_string.split(" ")] 

# Count the occurrences of each word
words_count = Counter(reviews_to_words)
print(f"The word counts from review: {words_count}")

# Select the 3 most common words and their counts
print(f"The 3 most common words: {words_count.most_common(3)}")

print("-" * 30)

##### Block 5: collections.defaultdict #####
print("\n--- Block 5: collections.defaultdict ---")

# --- defaultdict(list) ---
# Useful for grouping items

grouped_by_category = defaultdict(list)

products = [
    {"name": "Laptop", "category": "Electronics"},
    {"name": "Mouse", "category": "Electronics"},
    {"name": "Book", "category": "Books"},
    {"name": "Keyboard", "category": "Electronics"},
    {"name": "Pen", "category": "Stationery"}
]
for product in products:
    category = product["category"]
    grouped_by_category[category].append(product["name"]) # No need to check if category exists!

print(f"Products by category: {grouped_by_category}")

# Practical Problem 5.1: Grouping Student Enrollments
# Create a list of student enrollment records
enrollments = [
    {"student_id": 1, "course": "Math"},
    {"student_id": 2, "course": "Physics"},
    {"student_id": 1, "course": "Chemistry"},
    {"student_id": 3, "course": "Math"},
    {"student_id": 2, "course": "Chemistry"}
]
# Group Courses by Student:
grouped_by_student = defaultdict(list)

# Create a dictionary where keys are student_ids and values are lists of courses that student is enrolled in.
for item in enrollments:
    student = item["student_id"]
    grouped_by_student[student].append(item["course"])

# Print the resulting dictionary
print(f"Courses by student ID: {grouped_by_student}")

# Useful for counting or summing when you don't use Counter
sales_data = [("Monday", 100), ("Tuesday", 150), ("Monday", 50)]
daily_sales = defaultdict(int)
for day, sale in sales_data:
    daily_sales[day] += sale # Initializes day to 0 if not present, then adds amount

# print(daily_sales) 

print("-" * 30)

##### Block 6: Advanced Combined Problem #####
print("\n--- Block 6: Advanced Combined Problem ---")

# Practical Problem 6.1: Sales Transaction Analysis

# 1. Create a list of sales transactions
transactions = [
    {"transaction_id": "T001", "product_id": "P101", "quantity": 2, "status": "completed"},
    {"transaction_id": "T002", "product_id": "P102", "quantity": 1, "status": "pending"},
    {"transaction_id": "T003", "product_id": "P101", "quantity": 3, "status": "completed"},
    {"transaction_id": "T004", "product_id": "P103", "quantity": 1, "status": "failed"},
    {"transaction_id": "T005", "product_id": "P102", "quantity": 2, "status": "completed"},
    {"transaction_id": "T006", "product_id": "P101", "quantity": 1, "status": "pending"}
]
print("\nSales Transactions Data:")
for log in transactions:
    print(f"- {log}")

# 2. Part A: Group Transactions by Product (using defaultdict)
# Create a defaultdict(list) called transactions_by_product
transactions_by_product = defaultdict(list)

# Iterate through transactions and group all transactions under their respective product_id
for log in transactions:
    product = log["product_id"]
    transactions_by_product[product].append(log)

print(f"\nPart A: Transactions Grouped by Product ID: {transactions_by_product}")

# 3. Part B: Count Transaction Statuses (using Counter)
# Create a Counter called status_counts
status_counts = Counter([log["status"] for log in transactions])
print(f"\nPart B: Transaction Status Counts: {status_counts}")
# Count how many times each status (e.g., "completed", "pending", "failed") appears.

# 4. Part C: Calculate Total Quantity Sold Per Product (using comprehension and grouped data)
total_quantity_sold = {product: sum([data["quantity"] for data in transaction if data["status"] == "completed"]) for product, transaction in transactions_by_product.items()}
print(f"\nPart C: Total Quantity of COMPLETED Sales Per Product: {total_quantity_sold}")

# 5. Part D: Find Products with Failed Transactions (using comprehension and sets)
# Create set that contain the product_ids of all products that have at least one transaction with status "failed"
products_with_failures = {transaction["product_id"] for transaction in transactions if transaction["status"] == "failed"}
print(f"\nPart D: Product IDs with Failed Transactions: {products_with_failures}")

print("-" * 30)