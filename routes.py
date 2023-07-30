from flask import Flask, render_template, request, redirect, url_for
from database import create_table, work_table
import sqlite3


app = Flask(__name__)


@app.route('/')
def home():
    """ This function uses the route / which renders index.html page with its data."""
    return render_template('index.html', active='home')


@app.route('/newtenant', methods=['GET', 'POST'])
def newtenant():
    """This function helps in inserting the tenant data whenever user submits the form
    with details filled out in form inside the newtenant.html. Using this, the function
    would acknowledge the user's action."""
    create_table()

    error_message = None

    if request.method == 'POST':
        apart_num = request.form.get('apt_num')
        name = request.form.get('name')
        rent = request.form.get('rent')
        ph_number = request.form.get('ph_num')

        try:
            apart_num = int(apart_num)
        except ValueError:
            error_message = 'Apartment Number should be a number.'

        try:
            rent = int(rent)
        except ValueError:
            error_message = 'Rent should be a number.'

        if error_message:
            return render_template('newtenant.html', active='new_tenant', form_submitted=False,
                                   error_message=error_message)

        if apart_num < 1800 or apart_num > 1899:
            error_message = 'Apartment Number should be between 1800 and 1899.'
            return render_template('newtenant.html', active='new_tenant', form_submitted=False,
                                   error_message=error_message)

        conn = sqlite3.connect('tenant_info.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM tenants WHERE apt_num=?', (apart_num,))
        num_existing_apartments = cursor.fetchone()[0]
        conn.close()

        if num_existing_apartments > 0:
            error_message = 'Tenant already exists.'
            return render_template('newtenant.html', active='new_tenant', form_submitted=False,
                                   error_message=error_message)

        conn = sqlite3.connect('tenant_info.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO tenants (apt_num, name, rent, ph_num)
                            VALUES (?, ?, ?, ?)''', (apart_num, name, rent, ph_number))
        conn.commit()
        conn.close()

        return render_template('newtenant.html', active='new_tenant', form_submitted=True)
    else:
        return render_template('newtenant.html', active='new_tenant', form_submitted=False)


@app.route('/viewtenant', methods=['GET', 'POST'])
def viewtenant():
    """This function would be able to search for the tenant's information based on the
    apartment number given in the search field. The results are sent to the viewtenant.html
    which then renders the data in table format and displays to the user."""
    success_message = request.args.get('success_message')
    error_message = None

    if request.method == 'POST':
        apart_num = request.form.get('search_apt_num')
        try:
            apart_num = int(apart_num)
        except ValueError:
            error_message = 'Apartment Number should be a number.'

        if error_message:
            return render_template('viewtenant.html', active='view_tenant', form_submitted=False,
                                   error_message=error_message)

        conn = sqlite3.connect('tenant_info.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tenants where apt_num= ?', (apart_num,))
        tenants = cursor.fetchall()
        conn.close()

        if not tenants:  # Check if the list is empty (no tenant found)
            no_tenant_message = f"No tenant found for Apartment Number: {apart_num}"
            return render_template('viewtenant.html', active='view_tenant', no_tenant_message=no_tenant_message,
                                   form_submitted=True)

        return render_template('viewtenant.html', active='view_tenant', tenants=tenants, form_submitted=True)
    else:
        return render_template('viewtenant.html', active='view_tenant', success_message=success_message,
                               form_submitted=False)


@app.route('/deletetenant/<int:tenant_id>', methods=['POST'])
def deletetenant(tenant_id):
    """This function is called when the user clicks on the delete button to delete an existing tenant.
    It will delete the tenant record from the database based on the provided apartment number."""

    conn = sqlite3.connect('tenant_info.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tenants WHERE id=?', (tenant_id,))
    conn.commit()
    conn.close()
    success_message = 'Tenant Successfully Deleted'
    return redirect(url_for('viewtenant', success_message=success_message))


@app.route('/workorders', methods=['GET', 'POST'])
def workorders():
    """This function is called when the user submits the form in workorders.html page filling
    out the information on the new work order. This function would then capture the information
     and the insert the data into the workorders table."""
    work_table()

    error_message = None

    if request.method == 'POST':
        apart_num = request.form.get('apt_num')
        issue = request.form.get('issue')
        status = request.form.get('status_issue')

        try:
            apart_num = int(apart_num)
        except ValueError:
            error_message = 'Apartment Number should be a number.'

        if error_message:
            return render_template('workorder.html', active='work_orders', form_submitted=False,
                                   error_message=error_message)

        if apart_num < 1800 or apart_num > 1899:
            error_message = 'Apartment Number should be between 1800 and 1899.'
            return render_template('workorder.html', active='work_orders', form_submitted=False,
                                   error_message=error_message)

        conn = sqlite3.connect('tenant_info.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO workorders (apt_num, issue, status)
                        VALUES (?, ?, ?)''', (apart_num, issue, status))
        conn.commit()
        conn.close()

        return render_template('workorder.html', active='work_orders', form_submitted=True)
    else:
        return render_template('workorder.html', active='work_orders', form_submitted=False)


@app.route('/viewworkorder', methods=['GET', 'POST'])
def viewworkorder():
    """This function is called when the user submits a form in the viewworkorder.html page.
    When user enters an apartment number in the search field and clicks on submit, it runs
    a prepared statement that retrieves the records and sends it back to the html page."""
    success_message = request.args.get('success_message')
    error_message = None

    if request.method == 'POST':
        apart_num = request.form.get('search_apt_num')
        try:
            apart_num = int(apart_num)
        except ValueError:
            error_message = 'Apartment Number should be a number.'

        if error_message:
            return render_template('viewworkorder.html', active='view_work_orders', form_submitted=False,
                                   error_message=error_message)

        conn = sqlite3.connect('tenant_info.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM workorders where apt_num= ?', (apart_num,))
        tenants = cursor.fetchall()
        conn.close()

        return render_template('viewworkorder.html', active='view_work_orders', tenants=tenants, form_submitted=True)
    else:
        return render_template('viewworkorder.html', active='view_work_orders', success_message=success_message,
                               form_submitted=False)


@app.route('/updatestatus/<int:order_id>', methods=['POST'])
def update_status(order_id):
    """This function is called when user tries to change the status of the issue and clicks
    on the update button in viewworkorder.html page. This would then update the status of the
    issue in the database. The page then redirects to initial viewworkorder page."""
    new_status = request.form.get('status')
    conn = sqlite3.connect('tenant_info.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE workorders SET status = ? WHERE id = ?', (new_status, order_id))
    conn.commit()
    success_message = 'Work Order Successfully Updated'
    conn.close()

    return redirect(url_for('viewworkorder', success_message=success_message))
