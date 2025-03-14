from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
import mysql.connector as mc
conn = mc.connect(user='root', password='SaniyaMirza@23', host='localhost', database='credit')
import joblib
model = joblib.load("randomforestclassifier.lb")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('userdata.html') 

@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if request.method == 'POST':
        income = request.form['income']
        limit = request.form['limit']
        cards = request.form['cards']
        age = int(request.form['age'])
        education = request.form['education']
        gender = request.form['gender']
        student = request.form['student']
        married = request.form['married']


        unseen_data = [[income, limit, cards, age, education, gender, student, married]]

        
        output = model.predict(unseen_data)[0] 

        
        query = """INSERT INTO customer(income, credit_limit, cards, age, education, gender, student, married, predicted)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        mycursor = conn.cursor()
        details = (income, limit, cards, age, education, gender, student, married, int(output))

        mycursor.execute(query, details)
        conn.commit()

        mycursor.close()

    
        return f"The predicted salary for the job is: {output}"

@app.route('/history')
def history():
    conn = mc.connect(user="root", host="localhost", password="SaniyaMirza@23", database='credit') 
    mycursor = conn.cursor()

    query = "SELECT * FROM customer"  
    mycursor.execute(query)


    data = mycursor.fetchall()

    mycursor.close()
    conn.close()

    return render_template('history.html', userdetails=data)


if __name__ == "__main__":
    app.run(debug=True)
