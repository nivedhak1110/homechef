
"""
This File helps to understand receiving the inputs from the HTML page
"""

# Method to read and verify user login credentials
def check_credentials(request):
    email_id = request.form.get('ID')
    passwd = request.form.get('password')
    
    if ("sdkarthikk@gmail.com" == email_id and "1234" == passwd):
        print("Login Succes !!", flush=True)
        return "success"
    elif("nv@gmail.com" == email_id and "nv" == passwd):
        print("Login Succes !!", flush=True)
        return "success"
        
        
        
    else:
       print("Invalid credentials, Login Failed", flush=True)
       return "failed"


# method to save the signup details
def save_details(request):
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('add')
    print("User details saved", flush=True)
    print(fname, lname, email, address, flush=True)
    return "success"

