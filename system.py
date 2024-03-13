# Objetive: save from HTML form to MySQL using python
# Flask- its a python Library/Framework for developing web applications
# Flask comes with predefined codes, developers write less codes

from flask import *
# Create a Flask app
app = Flask(__name__)

# Routing. This is the default route
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # We check if above email and password 
        import pymysql
        connection = pymysql.connect(host='localhost', user='root', password='', database='froyodb')
        
        sql = 'select * from register where email = %s and password = %s'
        cursor = connection.cursor()
        cursor.execute(sql, (email, password)) # replace placeholders with real values

        # Check how many rows the sql found,
        if cursor.rowcount == 0:
            return render_template('login.html', message = 'Wrong username/Password')
        elif cursor.rowcount == 1:
            return render_template('login.html', message = 'Welcome, Log in succesful')
        else:
            return render_template('login.html', message = 'Something went wrong, try again later')        

    
    else:
        return render_template('login.html')  # show the form to the user

# This route receives 5 variables posted by the form
# Post and get are methods for posting data from a form
@app.route('/book', methods = ['POST', 'GET'])
def book():
    if request.method == 'POST':
        departure = request.form['departure']
        destination = request.form['destination']
        date = request.form['date']
        time = request.form['time']
        amount = request.form['amount']

        import pymysql
        connection = pymysql.connect(host='localhost', user='root', password='', database='froyodb')
        print("Connection Established Successfully")


        sql = 'insert into bookings(departure,destination,date,time,amount) values(%s,%s,%s,%s,%s) '
        cursor = connection.cursor()
        cursor.execute(sql, (departure, destination, date, time, amount))
        connection.commit()
        return render_template('book.html', message = "Your booking was received.")

    else:   # Below display the form 
        return  render_template('book.html')   

# Sign up
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method =='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        phonenumber = request.form['phonenumber']

        if len(password1) < 8:
            return render_template('register.html', message = "Password must be 8 characters.")
        elif password1 != password2:
            return render_template('register.html', message = "Passwords do not match")    
        else:
            import pymysql
            connection=pymysql.connect(host='localhost', user='root', password='', database='froyodb')
            sql='insert into register(firstname,lastname,email,password,phonenumber)values(%s,%s,%s,%s,%s)'
            cursor = connection.cursor()
            cursor.execute(sql, (firstname, lastname, email, password1, phonenumber))
            connection.commit()
            return render_template('register.html', message = "Registration succesful")
    else:
        return render_template('register.html')        
        


@app.route('/view')
def view():
    import pymysql
    connection=pymysql.connect(host='localhost', user='root', password='', database='froyodb')
    sql = 'select * from bookings order by date desc'
    cursor = connection.cursor()
    cursor.execute(sql)

    if cursor.rowcount == 0:
        return render_template('view.html', message = "No Bookings")
    else:
        rows = cursor.fetchall()
        return render_template('view.html', rows = rows) # put rows in a variable
   


# Assume you have a task to do,to save a driver.
# 1. Driver Table
# 2. Route in python/savedriver
# 3. Template named savedriver.html

# run 127.0.0.1:5000/savedriver
# To do route here

@app.route('/savedriver', methods = ['POST', 'GET'])
def savedriver():
    if request.method == 'POST':
        driver_name = request.form['driver_name']
        driver_phone = request.form['driver_phone']
        idnumber = request.form['idnumber']
        car_assigned = request.form['car_assigned']

        import pymysql
        connection = pymysql.connect(host='localhost', user='root', password='', database='froyodb')
        print("Connection Established Successfully")

        sql = 'insert into driver(driver_name,driver_phone,idnumber,car_assigned) values(%s,%s,%s,%s) '
        cursor = connection.cursor()
        cursor.execute(sql, (driver_name, driver_phone, idnumber, car_assigned))
        connection.commit()
        return render_template('savedriver.html', message = "The driver was added succesfully.")

    else:   # Below display the form 
        return  render_template('savedriver.html') 





@app.route('/views')
def views():
    import pymysql
    connection=pymysql.connect(host='localhost', user='root', password='', database='froyodb')
    sql = 'select * from driver order by driver_id desc'
    cursor = connection.cursor()
    cursor.execute(sql)

    if cursor.rowcount == 0:
        return render_template('views.html', message = "No Driver Available")
    else:
        rows = cursor.fetchall()
        return render_template('views.html', rows = rows)



# Create a hire route
@app.route('/hire')
def hire():
    import pymysql
    connection=pymysql.connect(host='localhost', user='root', password='', database='froyodb')

    sql = "select * from hire where status = 'yes' "
    cursor = connection.cursor()
    cursor.execute(sql)

    if cursor.rowcount == 0:
        return render_template('hire.html', message = "No vehicles available now")
    else:
        rows = cursor.fetchall()
        return render_template('hire.html', rows = rows)  # Put rows in a variable  

# Below route receives a reg number
@app.route('/single/<reg>')
def single(reg):
    # We now deal with 1 car using the reg number provided
    # Write an sql to get all details of this car
     import pymysql
     connection=pymysql.connect(host='localhost', user='root', password='', database='froyodb')

     sql = "select * from hire where car_reg = %s "
     cursor = connection.cursor()
     cursor.execute(sql, (reg))
    #  From above you get 1 car with given reg
     row = cursor.fetchone()
    #  We then return the row to a new template named single.html
     return render_template('single.html', row = row)

# https://github.com/modcomlearning/mpesa_sample
# Click on the app.py
import requests     # Used to post to safaricom url
import datetime     # Get current time
import base64       # Encoding scheme to auhenticate data 
from requests.auth import HTTPBasicAuth
# Copy from line 7 to 58
@app.route('/mpesa', methods = ['POST','GET'])
def mpesa_payment():
        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])
            # GENERATING THE ACCESS TOKEN
            # We get them from daraja portal
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json() 
            # Below token is used to secure your transactions
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"    # Test paybill. Change to yours
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return 'Please Complete Payment in Your Phone'
        else:
            return redirect('/hire')





app.run(debug=True)
# To access flask app,open a browser and type  ; http://127.0.0.1:5000/