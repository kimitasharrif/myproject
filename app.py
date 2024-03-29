from flask import*
import pymysql
# creating the app
app=Flask(__name__)
# define the secret key
app.secret_key='erth@.,bhjfvbdcv)9bn&%$#28sdfgjkjhkjh' 
# Define the connection
connection=pymysql.connect(host="localhost",user="root", database="bookings_db",password="")
# create the main
@app.route("/")
def Main():
    return render_template ( "index.html" )
# create the room-upload route
@app.route("/upload_room",methods=['GET','POST'])
def Upload_room():
    # if 'key_admin' not in session:
        #  return redirect("/admin")
    # check if user has posted anything
    if request.method == 'POST':
        # TODO
        
        # To get erecords from the user/form
        room_name=request.form['room_name']
        room_desc=request.form['room_desc']
        cost=request.form['cost']
        availability=request.form['availability']
        square_feet=request.form['square_feet']
        # image=request.files['image_url']
        image_url=request.form['image_url']
        # check if user has filled all the records
        if not room_name or not room_desc or not cost or not availability or not square_feet:# or not image
            return render_template("upload_room.html",error="Please fill all the record")
        # save the image inside static folder
        # image.save('static/images/'+image.filename)
        # pick  the name of the image
        # image_url=image.filename
        # create cursor-to executethe sql query
        cursor=connection.cursor()
        # define the sql query
        sql='insert into rooms(room_name,room_desc, cost, availability,square_feet,image_url) values(%s,%s,%s,%s,%s,%s)'
        values=(room_name,room_desc,cost,availability,square_feet,image_url)
        # execute the sql query
        cursor.execute(sql,values)
        connection.commit()
        return render_template("upload_room.html",message="Room uploaded successifully")
    return render_template("upload_room.html")
# crud operation
# c-create, save records  -==methods=POST
# r-read- select,retrieve,view      =GET
#  u-update-edit                    =PUT
# d-delete-remove                   =DELETE
@app.route("/getrooms", methods=['GET','POST'])
def Get_rooms():
    # define the connection
    sql='select* from rooms'
    # cursor function to execute the sql
    cursor=connection.cursor()
    # execute the sql query
    cursor.execute(sql)
    # fetch the records
    records=cursor.fetchall()
    # check if there are records saved in the database
    if cursor.rowcount ==0:
        return render_template("rooms.html",error="No rooms available")
    else:
      return render_template("rooms.html",rooms=records)
    #   return jsonify(records)



    

# admin get rooms




# signup route
@app.route("/signup",methods=['GET','POST'])
def Signup():
    # Get the data from the form
    if request.method == 'POST':
        #TODO
        # Get the data from the table
        username=request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if not username or not email or not phone or not password or not confirm_password :
                    return render_template("signup.html",error="Please fill all the record")
        if password !=confirm_password:
                return render_template("signup.html",error="Password do not match confirm password")
        elif " " in username:
                return render_template ("signup.html", 'username must be one word')
        elif '@' not in email:
                return render_template("signup.html", 'email must have @')
        elif len(password) <4:
                return render_template("signup.html", 'password must have four digits')
        else:
            # check if user exist
            sql_check_user='select* from users where  username=%s'
            cursor_check_user=connection.cursor()
            cursor_check_user.execute(sql_check_user, username)
            if cursor_check_user.rowcount==1:
                 return render_template("signup.html",error="Username already exist")
            
            sql_save='insert into users (username,email,phone ,password) values(%s,%s,%s,%s)'
            values=(username,email,phone,password)
            # cursor function 
            cursor_save=connection.cursor()
            #execute the sql query
            cursor_save.execute(sql_save,values)
            # commit
            connection.commit()
            return render_template("signup.html", message="Signup successifully")
    else: 
       return render_template("signup.html")   
  # sign in route
@app.route("/login",methods=['GET','POST'])
def Signin():
     # check the method
     if request.method=='POST':
          # TODO
          username=request.form['username']
          password=request.form['password'] 
          # define sql query
          sql='select* from users where username=%s and password=%s'   
          # create a cursor function
          cursor=connection.cursor()
          # execute tthe sql
          cursor.execute(sql, (username,password))
          if cursor.rowcount==0:
            return render_template("signup.html",error="Incorect log in details. Please try again")    
            #   return render_template("signup.html", message="Log in successifully") 
         # create users session
          session['key']=username
          #fetch other columns
          user=cursor.fetchone()
          session['email']=user[1]
          session['phone']=user[2]
          return redirect("/getrooms")
     else:
        return render_template("signup.html")      
# clear  the session
@app.route("/logout")
def Logout():
     session.clear()
     return redirect("/")
@app.route("/logout_admin")
def Logout_admin():
     session.clear()
     return redirect("/admin")

# log inroute for the admin
@app.route("/admin",methods=['GET','POST'])
def Admin():
     # check the method
     if request.method=='POST':
          # TODO
          username=request.form['username']
          password=request.form['password'] 
          # define sql query
          sql='select* from users where username=%s and password=%s'   
          # create a cursor function
          cursor=connection.cursor()
          # execute tthe sql
          cursor.execute(sql, (username,password))
          # check if user exist
          if cursor.rowcount==0:
               return render_template("admin.html",error="Incorect log in details. Please try again")   
          admin=cursor.fetchone()
          role=admin[0]
          if role != 'admin':
               return render_template("admin.html",error="Incorect log in details. Please try again")   
         #   return render_template("signup.html", message="Log in successifully") 
         # create users session
          session['key_admin']=username
          #fetch other columns
          user=cursor.fetchone()
          print(user)
          session['email_admin']=admin[1]
          session['phone_admin']=admin[2]
          return redirect("/admin_dash")
     else:
        return render_template("admin.html")      
# Single item route
@app.route("/single_room/<room_id>",methods=['GET','POST'])
def Single_item(room_id):
     # check if user has sign in/session is live
     if 'key' not in session:
          return redirect ("/login")
     else:
          # Define the sql query
         sql='select* from rooms where room_id=%s'
          # create the cursor function
         cursor=connection.cursor()
         cursor.execute(sql, room_id)
         # check if products exists
         if cursor.rowcount==0:
              return render_template("single_item.html", error="Products does not exist")
         # fetch the product info
         room=cursor.fetchone()
         # return the variable room
     #     return jsonify(room)
         return render_template("single_item.html",data=room)
      
# mpesa intergration route
# mpesa integration route
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
@app.route("/mpesa_payment",methods=['POST','GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379" #test paybil
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount":amount,  # use 1 when testing
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

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href='' class="btn btn-dark btn-sm">Back to Products</a>'
    else:
        return render_template("single_item.html")

@app.route("/view_rooms", methods=['GET','POST'])
def View_rooms():
    # define the connection
    sql='select* from rooms'
    # cursor function to execute the sql
    cursor=connection.cursor()
    # execute the sql query
    cursor.execute(sql)
    # fetch the records
    records=cursor.fetchall()
    # check if there are records saved in the database
    if cursor.rowcount ==0:
        return render_template("view_rooms.html",error="No rooms available")
    else:
      return render_template("view_rooms.html",rooms=records)
    


@app.route("/admin_dash", methods=['GET','POST'])
def Admin_dash():
    if 'key_admin' not in session:
         return redirect("/admin")
    # define the connection
    sql='select* from rooms'
    # cursor function to execute the sql
    cursor=connection.cursor()
    # execute the sql query
    cursor.execute(sql)
    # fetch the records
    records=cursor.fetchall()
    # check if there are records saved in the database
    if cursor.rowcount ==0:
        return render_template("admin_dash.html",error="No rooms available")
    else:
      return render_template("admin_dash.html",rooms=records)
    

@app.route("/delete<room_id>",methods=('GET','POST'))
def Delete_room(room_id):
     # define the sql for deleting the records
     sql='delete from rooms where room_id=%s'
     # cusor
     cursor=connection.cursor()
     # execute the sql
     cursor.execute(sql,room_id)
     #  commit the connection
     connection.commit()
     return redirect("/view_rooms")    


# import functions from functions.py file
from functions import *
from order_gen import *
# add to cart route
@app.route('/add', methods=['POST'])
def add_product_to_cart():
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        # validate the received values
        if _quantity and _code and request.method == 'POST':
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM rooms WHERE room_id= %s", _code)
            row = cursor.fetchone()
            #An array is a collection of items stored at contiguous memory locations. The idea is to store multiple items of the same type together

            itemArray = {str(row['room_id']): {'room_name': row['room_name'], 'room_id': row['room_id'], 'quantity': _quantity, 'cost': row['cost'],
                              'image_url': row['image_url'], 'total_price': int(_quantity) * int(row['cost']),
                                             'Availability': row['availability']}}
            print((itemArray))


            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            #if there is an item already
            if 'cart_item' in session:
                #check if the product you are adding is already there
                print("The test cart",type(row['room_id']) )
                print("session hf", session['cart_item'])
                if str(row['room_id']) in session['cart_item']:
                    print("reached here 1")


                    for key, value in session['cart_item'].items():
                        #check if product is there
                        if str(row['room_id']) == key:
                            print("reached here 2")
                            #take the old quantity  which is in session with cart item and key quantity
                            old_quantity = int(session['cart_item'][key]['quantity'])
                            #add it with new quantity to get the total quantity and make it a session
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            #now find the new price with the new total quantity and add it to the session
                            session['cart_item'][key]['total_price'] = total_quantity *  row['cost']

                else:
                    print("reached here 3")
                    #a new product added in the cart.Merge the previous to have a new cart item with two products
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)


                for key, value in session['cart_item'].items():
                    individual_quantity = session['cart_item'][key]['quantity']
                    individual_price = session['cart_item'][key]['total_price']
                    all_total_quantity = all_total_quantity +individual_quantity
                    all_total_price = int(all_total_price) +int(individual_price)
            else:
                #if the cart is empty you add the whole item array
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                #get total price by multiplyin the cost and the quantity
                all_total_price = all_total_price + _quantity* float(row['cost'])


            #add total quantity and total price to a session
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            return redirect(url_for('.cart'))
        else:
            return 'Error while adding item to cart'
       
@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/customer_checkout')
def customer_checkout():
    if check_customer():
            return redirect('/cart')
    else:
        return redirect('/login')
@app.route('/empty')
def empty_cart():
    try:
        if 'cart_item' in session or 'all_total_quantity' in session or 'all_total_price' in session:
            session.pop('cart_item', None)
            session.pop('all_total_quantity', None)
            session.pop('all_total_price', None)
            return redirect(url_for('.cart'))
        else:
            return redirect(url_for('.cart'))

    except Exception as e:
        print(e)
@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = int(all_total_price) + int(individual_price)
                break

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        # return redirect('/')
        return redirect(url_for('.cart'))
    except Exception as e:
        print(e)
# RUN THE APP
app.run(debug=True,port=8800)
