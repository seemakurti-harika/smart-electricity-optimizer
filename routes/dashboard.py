from flask import (
    render_template,
    redirect,
    session
)
import joblib
from app import app

from models.database import (
    get_db_connection
)

from utils.recommendations import (
    generate_ai_insights
)

from utils.billing import (
    calculate_bill,
    calculate_peak_tariff,
    calculate_savings
)
forecast_model = joblib.load(
    'ml/energy_forecast.pkl'
)

# DASHBOARD
@app.route('/dashboard')
def dashboard():

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

    reminders = conn.execute(
        '''
        SELECT * FROM reminders
        WHERE user_id=?
        ORDER BY reminder_time ASC
        ''',
        (session['user_id'],)
    ).fetchall()

    conn.close()

    # ====================================
    # BASIC ANALYTICS
    # ====================================

    total_appliances = len(appliances)

    total_units = round(sum(

        appliance['units']
        for appliance in appliances

    ), 2)

    # SMART SLAB BILLING

    total_bill = calculate_bill(
        total_units
    )

    average_units = round(

        total_units / total_appliances,
        2

    ) if total_appliances > 0 else 0

    # ====================================
    # CARBON ANALYTICS
    # ====================================

    carbon_emission = round(
        total_units * 0.82,
        2
    )

    trees_required = round(
        carbon_emission / 21,
        2
    )

    if carbon_emission < 50:

        sustainability_status = "Excellent"

        sustainability_color = "success"

    elif carbon_emission < 120:

        sustainability_status = "Moderate"

        sustainability_color = "warning"

    else:

        sustainability_status = "High Carbon Impact"

        sustainability_color = "danger"

    sustainability_score = max(

        0,

        round(
            100 - (carbon_emission / 2)
        )
    )

    # ====================================
    # EFFICIENCY SCORE
    # ====================================

    if total_units < 20:

        efficiency_score = 90
        efficiency_status = "Efficient"
        efficiency_color = "success"

    elif total_units < 50:

        efficiency_score = 70
        efficiency_status = "Moderate"
        efficiency_color = "warning"

    else:

        efficiency_score = 40
        efficiency_status = "High Consumption"
        efficiency_color = "danger"

    # ====================================
    # APPLIANCE ANALYTICS
    # ====================================

    appliance_names = []
    appliance_units = []

    highest_appliance = "None"
    highest_units = 0

    appliance_contributions = []

    for appliance in appliances:

        appliance_names.append(
            appliance['appliance_name']
        )

        appliance_units.append(
            appliance['units']
        )

        # HIGHEST CONSUMER

        if appliance['units'] > highest_units:

            highest_units = appliance['units']

            highest_appliance = appliance[
                'appliance_name'
            ]

        # CONTRIBUTION %

        if total_units > 0:

            contribution = round(

                (
                    appliance['units']
                    / total_units
                ) * 100,

                2
            )

        else:

            contribution = 0

        appliance_contributions.append({

            'name': appliance['appliance_name'],

            'units': appliance['units'],

            'contribution': contribution
        })

    # SORT HIGHEST FIRST

    appliance_contributions = sorted(

        appliance_contributions,

        key=lambda x: x['contribution'],

        reverse=True
    )

    # ====================================
    # MONTHLY ANALYTICS
    # ====================================

    monthly_data = {}

    for appliance in appliances:

        date = appliance['created_at'][:10]

        if date in monthly_data:

            monthly_data[date] += appliance['units']

        else:

            monthly_data[date] = appliance['units']

    monthly_dates = list(
        monthly_data.keys()
    )

    monthly_units = list(
        monthly_data.values()
    )

    # ====================================
    # CATEGORY ANALYTICS
    # ====================================

    category_data = {}

    for appliance in appliances:

        category = appliance['category']

        if category in category_data:

            category_data[category] += appliance['units']

        else:

            category_data[category] = appliance['units']

    category_names = list(
        category_data.keys()
    )

    category_units = list(
        category_data.values()
    )

    # ====================================
    # FUTURE PREDICTION
    # ====================================

    if len(monthly_units) > 0:

        recent_usage = monthly_units[-3:]

        predicted_units = round(

            sum(recent_usage)
            / len(recent_usage),

            2
        )

    else:

        predicted_units = 0

    predicted_bill = calculate_bill(
        predicted_units
    )

    # ====================================
    # PEAK TARIFF LOGIC
    # ====================================

    peak_tariff_active, peak_extra_charge = \
        calculate_peak_tariff(
            predicted_units
        )

    predicted_bill += peak_extra_charge

    predicted_bill = round(
        predicted_bill,
        2
    )

    # ====================================
    # SAVINGS ESTIMATION
    # ====================================

    estimated_savings = calculate_savings(
        total_bill
    )

    if estimated_savings > 0:

        savings_message = (

            f"You can save approximately "
            f"₹{estimated_savings} monthly "
            f"by optimizing appliance usage."
        )

    else:

        savings_message = (
            "Your energy usage is already optimized."
        )

    # ====================================
    # AI INSIGHTS
    # ====================================

    ai_insights = generate_ai_insights(

        appliances,

        total_units,

        total_bill
    )

    # ====================================
    # APPLIANCE HEALTH PREDICTION
    # ====================================

    health_predictions = []

    for appliance in appliances:

        appliance_name = appliance[
            'appliance_name'
        ]

        units = appliance['units']

        hours = appliance['hours']

        power = appliance['power']

        # OVERUSAGE DETECTION

        if hours >= 10:

            health_predictions.append(

                f"{appliance_name} may require "
                f"maintenance due to excessive runtime."
            )

        # HIGH POWER DETECTION

        if power >= 2500:

            health_predictions.append(

                f"{appliance_name} is drawing "
                f"very high power consistently."
            )

        # INEFFICIENCY DETECTION

        if units >= 20:

            health_predictions.append(

                f"{appliance_name} shows abnormal "
                f"energy consumption patterns."
            )

        # AC ANALYSIS

        if appliance_name.lower() == 'ac':

            if hours >= 8:

                health_predictions.append(

                    "AC efficiency may be decreasing. "
                    "Filter cleaning recommended."
                )

        # REFRIGERATOR ANALYSIS

        if appliance_name.lower() == 'refrigerator':

            if units >= 15:

                health_predictions.append(

                    "Refrigerator compressor may "
                    "require inspection."
                )

    # ====================================
    # ALERTS & RECOMMENDATIONS
    # ====================================

    recommendations = []

    alerts = []

    peak_alert = False

    for appliance in appliances:

        # HIGH USAGE

        if appliance['units'] > 10:

            recommendations.append(

                f"{appliance['appliance_name']} "
                f"is consuming high electricity."
            )

        elif appliance['units'] > 5:

            recommendations.append(

                f"Reduce usage time for "
                f"{appliance['appliance_name']}."
            )

        # PEAK ALERT

        if appliance['units'] > 15:

            peak_alert = True

        # AC TIP

        if appliance['appliance_name'].lower() == 'ac':

            recommendations.append(

                "Use AC at 24°C for "
                "better energy efficiency."
            )

        # WASHING MACHINE TIP

        if appliance[
            'appliance_name'
        ].lower() == 'washing machine':

            recommendations.append(

                "Run washing machine "
                "during low tariff hours."
            )

        # HIGH POWER ALERT

        if appliance['power'] >= 2000:

            alerts.append(

                f"⚠ {appliance['appliance_name']} "
                f"is consuming extremely high power."
            )

        # HIGH UNIT ALERT

        if appliance['units'] >= 15:

            alerts.append(

                f"⚠ Peak usage detected in "
                f"{appliance['appliance_name']}."
            )

        # LONG HOURS ALERT

        if appliance['hours'] >= 8:

            alerts.append(

                f"⚠ {appliance['appliance_name']} "
                f"is running continuously "
                f"for long hours."
            )

        # APPLIANCE HEALTH WARNING

        if appliance['hours'] >= 10:

            alerts.append(

                f"⚠ {appliance['appliance_name']} "
                f"may be operating inefficiently."
            )

    # HIGH BILL ALERT

    if total_bill >= 5000:

        alerts.append(

            "⚠ Your electricity bill "
            "is becoming extremely high."
        )

    # PEAK TARIFF ALERT

    if peak_tariff_active:

        alerts.append(

            "⚠ Peak-hour tariff "
            "is currently active."
        )

    # ====================================
    # RENDER TEMPLATE
    # ====================================

    return render_template(

        'dashboard.html',

        username=session['username'],

        total_appliances=total_appliances,

        total_units=total_units,

        total_bill=total_bill,

        average_units=average_units,

        highest_appliance=highest_appliance,

        appliance_names=appliance_names,

        appliance_units=appliance_units,

        category_names=category_names,

        category_units=category_units,

        monthly_dates=monthly_dates,

        monthly_units=monthly_units,

        efficiency_score=efficiency_score,

        efficiency_status=efficiency_status,

        efficiency_color=efficiency_color,

        carbon_emission=carbon_emission,

        trees_required=trees_required,

        sustainability_status=sustainability_status,

        sustainability_color=sustainability_color,

        sustainability_score=sustainability_score,

        predicted_units=predicted_units,

        predicted_bill=predicted_bill,

        estimated_savings=estimated_savings,

        savings_message=savings_message,

        peak_tariff_active=peak_tariff_active,

        peak_alert=peak_alert,

        recommendations=recommendations,

        alerts=alerts,

        reminders=reminders,

        ai_insights=ai_insights,

        appliance_contributions=appliance_contributions,

        health_predictions=health_predictions
    )


# PROFILE PAGE
@app.route('/profile')
def profile():

    if 'user_id' not in session:

        return redirect('/login')

    conn = get_db_connection()

    user = conn.execute(
        '''
        SELECT * FROM users
        WHERE id=?
        ''',
        (session['user_id'],)
    ).fetchone()

    appliances = conn.execute(
        '''
        SELECT * FROM appliances
        WHERE user_id=?
        ''',
        (session['user_id'],)
    ).fetchall()

    conn.close()

    total_appliances = len(appliances)

    total_units = round(sum(

        appliance['units']
        for appliance in appliances

    ), 2)

    total_bill = calculate_bill(
        total_units
    )

    return render_template(

        'profile.html',

        user=user,

        total_appliances=total_appliances,

        total_units=total_units,

        total_bill=total_bill
    )