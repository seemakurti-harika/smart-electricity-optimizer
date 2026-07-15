import pandas as pd
import random

data = []

appliances = [

    ("AC", 1500, 3000, 6, 12),

    ("Fan", 50, 100, 5, 20),

    ("TV", 80, 250, 2, 10),

    ("Refrigerator", 150, 400, 10, 24),

    ("Washing Machine", 400, 1000, 1, 3),

    ("Laptop", 40, 120, 3, 12),

    ("Microwave", 800, 2000, 0.2, 1),

    ("Iron", 700, 1800, 0.5, 2)
]

for i in range(1000):

    appliance = random.choice(appliances)

    appliance_name = appliance[0]

    power = random.randint(
        appliance[1],
        appliance[2]
    )

    hours = round(
        random.uniform(
            appliance[3],
            appliance[4]
        ),
        2
    )

    units = round(
        (power * hours) / 1000,
        2
    )

    # SLAB BILLING

    if units <= 100:

        rate = 5

    elif units <= 300:

        rate = 8

    else:

        rate = 12

    bill = round(
        units * rate,
        2
    )

    # PEAK HOUR CHARGE

    peak_usage = random.choice(
        [True, False]
    )

    if peak_usage:

        bill += 150

    data.append([

        appliance_name,
        power,
        hours,
        units,
        bill
    ])

df = pd.DataFrame(

    data,

    columns=[

        'Appliance',
        'Power',
        'Hours',
        'Units',
        'Bill'
    ]
)

df.to_csv(

    'dataset/energy_data.csv',

    index=False
)

print("Dataset Generated Successfully")