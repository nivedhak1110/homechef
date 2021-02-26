from flask import Flask, jsonify, render_template, redirect
from flask import request
from flask_cors import CORS
from core.logic import helper_nodb
from core.logic import helper
import hashlib



app: Flask = Flask(__name__)
CORS(app)


#username check method
@app.route('/usernamecheck', methods=['GET','POST'] )
def usernamecheck():
    if request.method == "POST":

        print(request)
        username = request.form['username']
        print(username)
        print(type(username))
        helper.create_database_myhomechef()
        helper.create_table_signup()
        status = helper.username_check(username)
        return  jsonify(status= status)


# signup page
@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup_design1.html')

@app.route('/demo')
def demo():
    return jsonify(message= "demoAPI")
# Saving signup details

@app.route('/signupsave',methods= ['POST'])
def save():
    if(request.method == 'POST'):
        helper.create_database_myhomechef()
        helper.create_table_signup()
        print(request)
        name = request.form['name']
        print(name)
        username = request.form['username']
        email = request.form['email']
        a = request.form['password']
        hash1 = hashlib.md5(a.encode())
        password = hash1.hexdigest()
        print(password)
        category = request.form['category']
        address = request.form['address']
        status = helper.signup_insert(name,username,email,password,category,address)
        return jsonify(status=status)


# Login  page

@app.route('/login')
def login():
    return render_template('login_design1.html')


#login check method
@app.route('/logincheck' , methods=['GET','POST'])
def logincheck():
    status = helper.read_input(request)
    print(status)
    if (status == "homechef"):
        return render_template('homechef-dashboard.html')
    elif(status == "customer"):
        return redirect("http://localhost:5000/restclient", code=302)


    else:
        return jsonify(status= 'Invalid credentials, Failed to login , Please try again', code=400)

# return Homechef dashboard to add more dishes

@app.route('/add_dish' ,methods=['post'] )
def homechef():

    helper.create_table_homechef()
    status = helper.get_input_homechef(request)
    if (status == "success"):
        return render_template('homechef-dashboard.html')
    else:
        return jsonify(status='Failed to save the details, try Signup Again', code=400)

# save homechef entries  page

@app.route('/homechef_save',methods=['post'])
def homechef_save():


    helper.create_table_homechef()
    status = helper.get_input_homechef(request)


    if (status == "success"):
        return render_template('homechef-dashboard.html')
    else:
        return jsonify(status='Failed to save the details, try Signup Again', code=400)
# render customer dashboard
@app.route('/restclient', methods = ['GET', 'POST'])
def restclient_test():
    return render_template('customer_dashboard.html')

# method to  return homechef id
@app.route('/test',methods=['get', 'POST'])
def test_get():
    list = helper.print_homechef_ID(request)

    return jsonify( name = list)


#method to get dishnames  from a particular chef_ID
@app.route("/get/dishname/<name>")
def get_dishname(name):
    try:
        # homechefname = name
        print(name)

        dish_names = helper.dish_names(name)
        return jsonify(chef_ID=name, dishnames =  dish_names )


    except Exception as exception:
        return jsonify(status=exception.args[0], code=500)


# Method to get the homechef details

@app.route("/dishdetails", methods = ['GET', 'POST'])
def get_dish():
        try:
           #homechefname = name
           if request.method == 'POST':
               print(request)
               dish_details = request.get_json(force=True)

               chef_ID = dish_details['chef_ID']

               dish = dish_details['dish']

               dish_details = helper.dish_details(chef_ID,dish)

               chef_name = dish_details[0][0]
               dish = dish_details[0][1]
               cost = dish_details[0][2]
               availability = dish_details[0][3]
               contact = dish_details[0][4]

               return jsonify(chef_ID= chef_ID, chef_name=chef_name,dish=dish,cost=cost,availability=availability,contact = contact )
        except Exception as exception:
            return print("error",exception)
# place order

@app.route("/order" , methods = ['GET', 'POST'])
def place_order():
    try:
        if request.method == 'POST':
            print(request)
            order_details = request.get_json(force=True)
            chef_ID = order_details['chef_ID']
            print(chef_ID)
            chef_name = order_details['chef_name']
            print(chef_name)
            dish = order_details['dish']
            print(dish)
            quantity = int(order_details['order_quantity'])
            print(quantity)
            customer_name = order_details['customer_name']
            print(customer_name)
            address = order_details['address']
            print(address)
            customer_contact = int(order_details['customer_contact'])
            print(customer_contact )
            current_availability = helper.place_order(chef_ID, quantity, dish)
            print(current_availability)

            if (current_availability >= 0):
                status = "success"
                print("create a order_details database and table")
                status1 = helper.create_table_order_details()

                if (status1 == "success"):
                    helper.insert_order_details(chef_ID,chef_name, customer_name, customer_contact, address, dish, quantity)
                else:
                    return jsonify(status='Failed to save the order details', code=400)
            else:
                status = "failed"

        if (status == "success"):
            return jsonify(response='thank you , your order placed!')
        else:
            return jsonify(response='sorry orders closed')


    except Exception as exception:
        return jsonify(status=exception.args[0], code=500)

#homechef check orders
@app.route('/check_orders', methods = ['GET', 'POST'])
def homechef_check_orders():
    return render_template('thankyou.html')
#method to retrive the name,order_details  of the customers who ordered the dish
@app.route('/customer_order_details' , methods = ['GET', 'POST'] )
def get_customer_order_details():
    try:
        if request.method == 'POST':
            print(request)
            dish_details = request.get_json(force=True)
            print(dish_details)
            chef_ID = dish_details['chef_ID']
            print(chef_ID)
            dish = dish_details['dish']
            print(dish)

            customer_order_details = helper.customer_order_details(chef_ID,dish)
            return jsonify(customer_order_details = customer_order_details)
    except Exception as exception:
        return jsonify(status=exception.args[0], code=500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

