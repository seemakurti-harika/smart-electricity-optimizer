from datetime import datetime


def calculate_bill(units):

    if units <= 100:

        rate = 5

    elif units <= 300:

        rate = 8

    else:

        rate = 12

    return round(units * rate, 2)


def calculate_peak_tariff(units):

    current_hour = datetime.now().hour

    peak_tariff_active = False

    extra_charge = 0

    # PEAK HOURS: 6 PM TO 10 PM

    if 18 <= current_hour <= 22:

        peak_tariff_active = True

        extra_charge = units * 2

    return peak_tariff_active, round(extra_charge, 2)


def calculate_savings(total_bill):

    estimated_savings = round(
        total_bill * 0.22,
        2
    )

    return estimated_savings