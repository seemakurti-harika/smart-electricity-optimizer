from flask import (
    session,
    redirect,
    make_response
)

from app import app

from models.database import (
    get_db_connection
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import colors


@app.route('/download_report')
def download_report():

    if 'user_id' not in session:

        return redirect('/login')

    conn = get_db_connection()

    appliances = conn.execute(
        '''
        SELECT * FROM appliances
        WHERE user_id=?
        ''',
        (session['user_id'],)
    ).fetchall()

    conn.close()

    pdf = SimpleDocTemplate(
        "energy_report.pdf"
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Smart Electricity Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    data = [[
        'Appliance',
        'Units',
        'Bill'
    ]]

    total_bill = 0

    for appliance in appliances:

        data.append([
            appliance['appliance_name'],
            appliance['units'],
            appliance['bill']
        ])

        total_bill += appliance['bill']

    table = Table(data)

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.grey),

        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),

        ('GRID', (0,0), (-1,-1), 1, colors.black)

    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    total = Paragraph(
        f"Total Bill: ₹ {round(total_bill, 2)}",
        styles['Heading2']
    )

    elements.append(total)

    pdf.build(elements)

    response = make_response(
        open("energy_report.pdf", "rb").read()
    )

    response.headers[
        'Content-Type'
    ] = 'application/pdf'

    response.headers[
        'Content-Disposition'
    ] = 'attachment; filename=energy_report.pdf'

    return response