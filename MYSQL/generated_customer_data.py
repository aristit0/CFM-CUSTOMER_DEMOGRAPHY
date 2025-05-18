import mysql.connector
from faker import Faker
import random
import time

# Configuration
MAX_CUSTOMERS = 5_000_000
BATCH_SIZE = 1000

# Initialize
fake = Faker()
seen_cifs = set()
inserted_total = 0

# MySQL connection
conn = mysql.connector.connect(
    user='root',
    password='Admin123',
    host='localhost',
    database='customer'
)
cursor = conn.cursor()

def generate_unique_cif():
    """Generate a unique CIF number."""
    while True:
        cif = random.randint(1000000000, 9999999999)
        if cif not in seen_cifs:
            seen_cifs.add(cif)
            return cif

def generate_data(batch_size=BATCH_SIZE):
    inserted = 0
    while inserted < batch_size:
        try:
            # Generate unique CIF
            cif = generate_unique_cif()
            name = fake.name()
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=75)
            gender = random.choice(['M', 'F'])
            address = fake.address().replace("\n", ", ")
            city = fake.city()

            # Insert into customer_info
            cursor.execute(
                "INSERT INTO customer_info (cif, name, birth_date, gender, address, city) VALUES (%s, %s, %s, %s, %s, %s)",
                (cif, name, birth_date, gender, address, city)
            )

            # Insert 1 bank product
            cursor.execute(
                "INSERT INTO bank_product (cif, product_type, open_date, status) VALUES (%s, %s, %s, %s)",
                (
                    cif,
                    random.choice(['SAVINGS', 'CREDIT_CARD', 'LOAN', 'DEPOSIT']),
                    fake.date_between(start_date='-5y', end_date='today'),
                    random.choice(['ACTIVE', 'CLOSED'])
                )
            )

            # Insert 1 asset
            cursor.execute(
                "INSERT INTO customer_asset (cif, asset_type, asset_value, valuation_date) VALUES (%s, %s, %s, %s)",
                (
                    cif,
                    random.choice(['PROPERTY', 'CAR', 'STOCKS', 'BONDS']),
                    round(random.uniform(10000, 500000), 2),
                    fake.date_between(start_date='-2y', end_date='today')
                )
            )

            inserted += 1

        except mysql.connector.Error as err:
            print(f"⚠️ MySQL error for CIF {cif}: {err}")
            continue  # Try next

# Main loop
while inserted_total < MAX_CUSTOMERS:
    generate_data()
    conn.commit()
    inserted_total += BATCH_SIZE
    print(f"✅ Inserted {inserted_total:,} of {MAX_CUSTOMERS:,} customers...")
    time.sleep(1)

print("🎉 Done generating 5 million customer records.")
conn.close()