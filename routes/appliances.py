from flask import (
    render_template,
    request,
    redirect,
    session,
    
)

import pandas as pd
import joblib

from app import app

from models.database import (
    get_db_connection
)

from utils.billing import (
    calculate_bill,
    calculate_peak_tariff
)

model = joblib.load('ml/model.pkl')


# ADD APPLIANCE
@app.route('/add_appliance', methods=['GET', 'POST'])
def add_appliance():

    if 'user_id' not in session:

        return redirect('/login')

    if request.method == 'POST':

        appliance_name = request.form['appliance_name']

        power = float(request.form['power'])

        hours = float(request.form['hours'])

        appliance_lower = appliance_name.lower()

        if appliance_lower in ['ac', 'fan', 'cooler']:

            category = 'Cooling'

        elif appliance_lower in ['tv', 'laptop', 'computer']:

            category = 'Electronics'

        elif appliance_lower in ['washing machine', 'iron']:

            category = 'Utility'

        elif appliance_lower in ['refrigerator', 'microwave']:

            category = 'Kitchen'

        else:

            category = 'General'

        input_data = pd.DataFrame(
            [[power, hours]],
            columns=['Power', 'Hours']
        )

        prediction = model.predict(input_data)

        units = round(prediction[0], 2)
        bill = calculate_bill(units)
        peak_active, peak_charge = \
            calculate_peak_tariff(units)
        bill += peak_charge
        bill = round(bill, 2)


        conn = get_db_connection()

        conn.execute(
            '''
            INSERT INTO appliances
            (
                user_id,
                appliance_name,
                power,
                hours,
                units,
                bill,
                category
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                session['user_id'],
                appliance_name,
                power,
                hours,
                units,
                bill,
                category
            )
        )

        conn.commit()

        conn.close()

        return redirect('/history')

    return render_template('add_appliance.html')


# HISTORY
@app.route('/history')
def history():

    if 'user_id' not in session:

        return redirect('/login')

    conn = get_db_connection()

    appliances = conn.execute(
        '''
        SELECT * FROM appliances
        WHERE user_id=?
        ORDER BY created_at DESC
        ''',
        (session['user_id'],)
    ).fetchall()

    conn.close()

    return render_template(
        'history.html',
        appliances=appliances
    )
    