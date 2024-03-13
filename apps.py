# create  a python program to save to our database
# Where is the database? user? password? database Name?
import pymysql 
def makebooking():
    connection = pymysql.connect(host='localhost', user='root', password='', database='froyodb')
    print("Connection Established Successfully")

    # create the variables you want to save to database
    departure = "Kisumu"
    destination = "Nairobi"
    date = "2022-06-12"
    time = "03:00"
    amount = "1400"

    # Do SQL, provide string placeholders %s for values
    # Below SQL is incomplete, since it has placeholders instead of values
    sql = 'insert into bookings(departure, destination, date, time, amount) values(%s,%s,%s,%s,%s) '

    # we now execute sql, cursor is used to execute/run sql in python
    # Note in below line cursor is using the connection
    cursor = connection.cursor()

    # Now execute, replace the placeholders with the values
    cursor.execute(sql, (departure, destination, date, time, amount))

    # Commit Changes
    connection.commit()
    print("Booking Updated to Database")


makebooking()    
