from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import DataRequired, Email, Length

# Define a WTForms Form for the contact validation
class ContactForm(FlaskForm):
    first_name = StringField('First Name', [Length(min=8)])
    last_name = StringField('Last Name', [Length(min=8)])
    phone = StringField('Phone', [DataRequired()])
    email = StringField('Email', [Email(), DataRequired()])


def initialize_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
           id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        email = form.email.data

        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (first_name, last_name, phone, email) VALUES (?, ?, ?, ?)", (first_name, last_name, phone, email))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        conn.close()
        return render_template('index.html', contacts=contacts, form=form)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    form = ContactForm(request.form)

    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        email = form.email.data
        cursor.execute("UPDATE contacts SET first_name=?, last_name=?, phone=?, email=? WHERE id=?", (first_name, last_name, phone, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT first_name, last_name, phone, email FROM contacts WHERE id=?", (id,))
        contact = cursor.fetchone()
        conn.close()
        form.first_name.data = contact[0]
        form.last_name.data = contact[1]
        form.phone.data = contact[2]
        form.email.data = contact[3]
        return render_template('edit.html', form=form, id=id)

if __name__ == "__main__":
    app.run(debug=True)
