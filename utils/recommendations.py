def generate_ai_insights(appliances, total_units, total_bill):

    insights = []

    if total_units == 0:

        return insights

    # HIGHEST CONSUMER
    highest_appliance = max(
        appliances,
        key=lambda x: x['units']
    )

    contribution = round(
        (highest_appliance['units'] / total_units) * 100,
        2
    )

    insights.append({

        "title": "Highest Energy Consumer",

        "message":
        f"{highest_appliance['appliance_name']} contributes "
        f"{contribution}% of total usage."
    })

    # SAVINGS
    estimated_savings = round(
        total_bill * 0.22,
        2
    )

    insights.append({

        "title": "Potential Savings",

        "message":
        f"You can save ₹{estimated_savings} "
        f"by optimizing appliance usage."
    })

    # HIGH BILL
    if total_bill > 3000:

        insights.append({

            "title": "High Electricity Bill",

            "message":
            "Your electricity bill is above average."
        })

    return insights