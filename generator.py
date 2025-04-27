import random
from datetime import datetime, timedelta

# first_names = ['Alice', 'Bob', 'Charlie', 'Daisy', 'Ethan']
# last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
# domains = ['example.com', 'test.com', 'demo.net']
#
# for _ in range(50):
#     first_name = random.choice(first_names)
#     last_name = random.choice(last_names)
#     email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
#     pin = random.randint(1000, 9999)
#     print(f"INSERT INTO employees (first_name, last_name, email, pin) VALUES ('{first_name}', '{last_name}', '{email}', '{pin}');")

sender_ids = range(101, 151)
receiver_ids = range(101, 151)
titles = ['Task X', 'Task Y', 'Task Z', 'Task Alpha', 'Task Beta']
bodies = ['Body X', 'Body Y', 'Body Z', 'Body Alpha', 'Body Beta']
references = ['Ref001', 'Ref002', 'Ref003', 'Ref004', 'Ref005']

start_date = datetime(datetime.now().year, 2, 1)

for _ in range(50):
    sender_id = random.choice(sender_ids)
    receiver_id = random.choice(receiver_ids)
    title = random.choice(titles)
    body = random.choice(bodies)
    reference = random.choice(references)
    creation_date = start_date - timedelta(days=random.randint(1, 30))
    due_date = start_date + timedelta(days=random.randint(1, 30))
    print(f"INSERT INTO tasks (sender_id, receiver_id, created_at, title, body, reference, due_at) VALUES ({sender_id}, {receiver_id}, '{creation_date.strftime('%Y-%m-%d %H:%M:%S')}', '{title}', '{body}', '{reference}', '{due_date.strftime('%Y-%m-%d %H:%M:%S')}');")
