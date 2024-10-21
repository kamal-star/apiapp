import frappe
import requests
import json
from frappe.utils import now

def post_customer_to_external_api(doc, method):
    # Define the API endpoints
    post_api_url = "http://195.200.14.68/hlf/customer/create"
    get_api_url = f"http://195.200.14.68/hlf/customer/get/{doc.name}"
    
    # Prepare the data to be sent to the external API
    customer_data = {
        "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
        "fullName": doc.customer_name,
        "customerType": doc.customer_type,
        "nationalIDNumber": doc.custom_national_id_numbereid,  # Placeholder, modify as needed
        "status": "Enabled",  # Assuming all new customers are active
        "modifiedBy": frappe.session.user,
        "createdBy": doc.owner,
        "createdDateTime": now().split(" ")[0],  # Current date in "YYYY-MM-DD" format
        "modifiedDateTime": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format
    }
    
    try:
        # Send the POST request
        post_response = requests.post(post_api_url, data=json.dumps(customer_data), headers={'Content-Type': 'application/json'})
        
        # Log the response details
        # frappe.log_error(f"POST Response Status Code: {post_response.status_code}", "API POST Response Status Code")
        # frappe.log_error(f"POST Response Text: {post_response.text}", "API POST Response Text")
        
        # Check for a successful response
        if post_response.status_code == 200:
            frappe.log_error("Customer data posted successfully to the external API.", "API POST Success")
            frappe.msgprint("Customer data posted successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            frappe.log_error(f"GET Response Status Code: {get_response.status_code}", "API GET Response Status Code")
            # frappe.log_error(f"GET Response Text: {get_response.text}", "API GET Response Text")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Customer",doc.name,"custom_validation",json.dumps(external_data))
                # doc.custom_validation = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                frappe.log_error("Customer data fetched and updated successfully from the external API.", "API GET Success")
                frappe.msgprint("Customer data fetched and updated successfully from the external API.", "API GET Success")
            else:
                frappe.log_error(f"Failed to fetch customer data. Status code: {get_response.status_code}, Response: {get_response.text}", "API GET Failure")
        else:
            frappe.log_error(f"Failed to post customer data. Status code: {post_response.status_code}, Response: {post_response.text}", "API POST Failure")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"An error occurred while communicating with the external API: {e}", "API Exception")

# Bind the function to the Customer doctype's after_insert event
# def register_custom_events():
#     frappe.connect_doc_events({
#         "Customer": {
#             "after_insert": post_customer_to_external_api
#         }
#     })

# register_custom_events()

def update_customer_status_and_fetch_data(doc, method):
    # Define the API endpoints
    stats=[]
    if doc.disabled==1:
        stats.append("Disabled")
    else:
        stats.append("Enabled")
    put_api_url = "http://195.200.14.68/hlf/customer/update-status"
    get_api_url = f"http://195.200.14.68/hlf/customer/get/{doc.name}"
    
    try:
        # Prepare data for the PUT request to update the status
        update_data = {
            "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
            "status": stats[0]  # Modify the status as needed
        }
        
        # Send the PUT request to update the status
        put_response = requests.put(put_api_url, data=json.dumps(update_data), headers={'Content-Type': 'application/json'})
        
        # Log the PUT response details
        frappe.log_error(title="API PUT Response Status Code", message=f"PUT Response Status Code: {put_response.status_code}")
        # frappe.log_error(title="API PUT Response Text", message=f"PUT Response Text: {put_response.text}")
        
        # Check for a successful PUT response
        if put_response.status_code == 200:
            frappe.log_error(title="API PUT Success", message="Customer status updated successfully in the external API.")
            frappe.msgprint("Customer data updated successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            frappe.log_error(title="API GET Response Status Code", message=f"GET Response Status Code: {get_response.status_code}")
            # frappe.log_error(title="API GET Response Text", message=f"GET Response Text: {get_response.text}")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Customer",doc.name,"custom_validation",json.dumps(external_data))
                # doc.external_api_data = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                frappe.log_error(title="API GET Success", message="Customer data fetched and updated successfully from the external API.")
                frappe.msgprint("Customer data pulled successfully to the external API.", "API POST Success")
            else:
                frappe.log_error(title="API GET Failure", message=f"Failed to fetch customer data. Status code: {get_response.status_code}, Response: {get_response.text}")
        else:
            frappe.log_error(title="API PUT Failure", message=f"Failed to update customer status. Status code: {put_response.status_code}, Response: {put_response.text}")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(title="API Exception", message=f"An error occurred while communicating with the external API: {e}")

# Bind the function to the Customer doctype's after_insert event


def post_hub_to_external_api(doc, method):
    # Define the API endpoints
    post_api_url = "http://195.200.14.68/hlf/hub/create"
    get_api_url = f"http://195.200.14.68/hlf/hub/get/{doc.name}"
    
    # Prepare the data to be sent to the external API
    hub_data = {
        "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
        "addressTitle": doc.address_line_1 + doc.address_line_2 ,
        "status": doc.status,  # Assuming all new customers are active
        "modifiedBy": frappe.session.user,
        "createdBy": doc.owner,
        "createdDateTime": now().split(" ")[0],  # Current date in "YYYY-MM-DD" format
        "modifiedDate": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format
    }
    
    try:
        # Send the POST request
        post_response = requests.post(post_api_url, data=json.dumps(hub_data), headers={'Content-Type': 'application/json'})
        
        # Log the response details
        # frappe.log_error(f"POST Response Status Code: {post_response.status_code}", "API POST Response Status Code")
        # frappe.log_error(f"POST Response Text: {post_response.text}", "API POST Response Text")
        
        # Check for a successful response
        if post_response.status_code == 200:
            frappe.log_error("Hub data posted successfully to the external API.", "API POST Success")
            frappe.msgprint("Hub data posted successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            
            # frappe.log_error(f"GET Response Text: {get_response.text}", "API GET Response Text")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Hub",doc.name,"validation",json.dumps(external_data))
                # doc.custom_validation = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                
                frappe.msgprint("HUB data fetched and updated successfully from the external API.", "API GET Success")
            else:
                frappe.log_error(f"Failed to fetch hub data. Status code: {get_response.status_code}, Response: {get_response.text}", "API GET Failure")
        else:
            frappe.log_error(f"Failed to post hub data. Status code: {post_response.status_code}, Response: {post_response.text}", "API POST Failure")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"An error occurred while communicating with the external API: {e}", "API Exception")

def update_hub_status_and_fetch_data(doc, method):
    # Define the API endpoints
    # stats=[]
    # if doc.disabled==1:
    #     stats.append("Disabled")
    # else:
    #     stats.append("Enabled")
    put_api_url = "http://195.200.14.68/hlf/hub/update-status"
    get_api_url = f"http://195.200.14.68/hlf/hub/get/{doc.name}"
    
    try:
        # Prepare data for the PUT request to update the status
        update_data = {
            "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
            "status": doc.status  # Modify the status as needed
        }
        
        # Send the PUT request to update the status
        put_response = requests.put(put_api_url, data=json.dumps(update_data), headers={'Content-Type': 'application/json'})
        
        # Log the PUT response details
        # frappe.log_error(title="API PUT Response Status Code", message=f"PUT Response Status Code: {put_response.status_code}")
        # frappe.log_error(title="API PUT Response Text", message=f"PUT Response Text: {put_response.text}")
        
        # Check for a successful PUT response
        if put_response.status_code == 200:
            # frappe.log_error(title="API PUT Success", message="Customer status updated successfully in the external API.")
            frappe.msgprint("Hub data updated successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            # frappe.log_error(title="API GET Response Status Code", message=f"GET Response Status Code: {get_response.status_code}")
            # frappe.log_error(title="API GET Response Text", message=f"GET Response Text: {get_response.text}")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Hub",doc.name,"validation",json.dumps(external_data))
                # doc.external_api_data = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                # frappe.log_error(title="API GET Success", message="Customer data fetched and updated successfully from the external API.")
                frappe.msgprint("Hub data pulled successfully to the external API.", "API POST Success")
            else:
                frappe.log_error(title="API GET Failure", message=f"Failed to fetch hub data. Status code: {get_response.status_code}, Response: {get_response.text}")
        else:
            frappe.log_error(title="API PUT Failure", message=f"Failed to update hub status. Status code: {put_response.status_code}, Response: {put_response.text}")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(title="API Exception", message=f"An error occurred while communicating with the external API: {e}")

def post_postoffice_to_external_api(doc, method):
    # Define the API endpoints
    post_api_url = "http://195.200.14.68/hlf/postoffice/create"
    get_api_url = f"http://195.200.14.68/hlf/postoffice/get/{doc.name}"
    
    # Prepare the data to be sent to the external API
    postoffice_data = {
        "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
        "addressTitle": doc.address_line_1 + " "+ doc.address_line_2 ,
        "status": doc.status,  # Assuming all new customers are active
        "modifiedBy": frappe.session.user,
        "createdBy": doc.owner,
        "createdDateTime": now().split(" ")[0],  # Current date in "YYYY-MM-DD" format
        "modifiedDate": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format
    }
    
    try:
        # Send the POST request
        post_response = requests.post(post_api_url, data=json.dumps(postoffice_data), headers={'Content-Type': 'application/json'})
        
        # Log the response details
        # frappe.log_error(f"POST Response Status Code: {post_response.status_code}", "API POST Response Status Code")
        # frappe.log_error(f"POST Response Text: {post_response.text}", "API POST Response Text")
        
        # Check for a successful response
        if post_response.status_code == 200:
            frappe.log_error("postoffice data posted successfully to the external API.", "API POST Success")
            frappe.msgprint("postoffice data posted successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            
            # frappe.log_error(f"GET Response Text: {get_response.text}", "API GET Response Text")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Post Office",doc.name,"validation",json.dumps(external_data))
                # doc.custom_validation = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                
                frappe.msgprint("postoffice data fetched and updated successfully from the external API.", "API GET Success")
            else:
                frappe.log_error(f"Failed to fetch postoffice data. Status code: {get_response.status_code}, Response: {get_response.text}", "API GET Failure")
        else:
            frappe.log_error(f"Failed to post postoffice data. Status code: {post_response.status_code}, Response: {post_response.text}", "API POST Failure")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"An error occurred while communicating with the external API: {e}", "API Exception")

def update_postoffice_status_and_fetch_data(doc, method):
    # Define the API endpoints
    # stats=[]
    # if doc.disabled==1:
    #     stats.append("Disabled")
    # else:
    #     stats.append("Enabled")
    put_api_url = "http://195.200.14.68/hlf/postoffice/update-status"
    get_api_url = f"http://195.200.14.68/hlf/postoffice/get/{doc.name}"
    
    try:
        # Prepare data for the PUT request to update the status
        update_data = {
            "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
            "status": doc.status  # Modify the status as needed
        }
        
        # Send the PUT request to update the status
        put_response = requests.put(put_api_url, data=json.dumps(update_data), headers={'Content-Type': 'application/json'})
        
        # Log the PUT response details
        # frappe.log_error(title="API PUT Response Status Code", message=f"PUT Response Status Code: {put_response.status_code}")
        # frappe.log_error(title="API PUT Response Text", message=f"PUT Response Text: {put_response.text}")
        
        # Check for a successful PUT response
        if put_response.status_code == 200:
            # frappe.log_error(title="API PUT Success", message="Customer status updated successfully in the external API.")
            frappe.msgprint("postoffice data updated successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            # frappe.log_error(title="API GET Response Status Code", message=f"GET Response Status Code: {get_response.status_code}")
            # frappe.log_error(title="API GET Response Text", message=f"GET Response Text: {get_response.text}")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Post Office",doc.name,"validation",json.dumps(external_data))
                # doc.external_api_data = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                # frappe.log_error(title="API GET Success", message="Customer data fetched and updated successfully from the external API.")
                frappe.msgprint("postoffice data pulled successfully to the external API.", "API POST Success")
            else:
                frappe.log_error(title="API GET Failure", message=f"Failed to fetch postoffice data. Status code: {get_response.status_code}, Response: {get_response.text}")
        else:
            frappe.log_error(title="API PUT Failure", message=f"Failed to update postoffice status. Status code: {put_response.status_code}, Response: {put_response.text}")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(title="API Exception", message=f"An error occurred while communicating with the external API: {e}")


def post_driver_to_external_api(doc, method):
    # Define the API endpoints
    post_api_url = "http://195.200.14.68/hlf/driver/create"
    get_api_url = f"http://195.200.14.68/hlf/driver/get/{doc.name}"
    
    # Prepare the data to be sent to the external API
    driver_data = {
        "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
        "userId": doc.employee,
        "fullname": doc.full_name,
        "licensenumber": doc.license_number,
        "expirydate": doc.expiry_date,
        "availability": doc.custom_availability,
        "drivertype": "Truck",
        "addressTitle": doc.address,
        "status": doc.status,  # Assuming all new customers are active
        "modifiedBy": frappe.session.user,
        "createdBy": doc.owner,
        "createdDateTime": now().split(" ")[0],  # Current date in "YYYY-MM-DD" format
        "modifiedDate": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format
    }
    
    try:
        # Send the POST request
        post_response = requests.post(post_api_url, data=json.dumps(driver_data), headers={'Content-Type': 'application/json'})
        
        # Log the response details
        # frappe.log_error(f"POST Response Status Code: {post_response.status_code}", "API POST Response Status Code")
        # frappe.log_error(f"POST Response Text: {post_response.text}", "API POST Response Text")
        
        # Check for a successful response
        if post_response.status_code == 200:
            frappe.log_error("driver data posted successfully to the external API.", "API POST Success")
            frappe.msgprint("driver data posted successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            
            # frappe.log_error(f"GET Response Text: {get_response.text}", "API GET Response Text")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Driver",doc.name,"custom_validation",json.dumps(external_data))
                # doc.custom_validation = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                
                frappe.msgprint("driver data fetched and updated successfully from the external API.", "API GET Success")
            else:
                frappe.log_error(f"Failed to fetch driver data. Status code: {get_response.status_code}, Response: {get_response.text}", "API GET Failure")
        else:
            frappe.log_error(f"Failed to post driver data. Status code: {post_response.status_code}, Response: {post_response.text}", "API POST Failure")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"An error occurred while communicating with the external API: {e}", "API Exception")

def update_driver_status_and_fetch_data(doc, method):
    # Define the API endpoints
    # stats=[]
    # if doc.disabled==1:
    #     stats.append("Disabled")
    # else:
    #     stats.append("Enabled")
    put_api_url = "http://195.200.14.68/hlf/driver/update-status"
    get_api_url = f"http://195.200.14.68/hlf/driver/get/{doc.name}"
    
    try:
        # Prepare data for the PUT request to update the status
        update_data = {
            "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
            "status": doc.status  # Modify the status as needed
        }
        
        # Send the PUT request to update the status
        put_response = requests.put(put_api_url, data=json.dumps(update_data), headers={'Content-Type': 'application/json'})
        
        # Log the PUT response details
        # frappe.log_error(title="API PUT Response Status Code", message=f"PUT Response Status Code: {put_response.status_code}")
        # frappe.log_error(title="API PUT Response Text", message=f"PUT Response Text: {put_response.text}")
        
        # Check for a successful PUT response
        if put_response.status_code == 200:
            # frappe.log_error(title="API PUT Success", message="Customer status updated successfully in the external API.")
            frappe.msgprint("driver data updated successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            # frappe.log_error(title="API GET Response Status Code", message=f"GET Response Status Code: {get_response.status_code}")
            # frappe.log_error(title="API GET Response Text", message=f"GET Response Text: {get_response.text}")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Driver",doc.name,"custom_validation",json.dumps(external_data))
                # doc.external_api_data = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                # frappe.log_error(title="API GET Success", message="Customer data fetched and updated successfully from the external API.")
                frappe.msgprint("driver data pulled successfully to the external API.", "API POST Success")
            else:
                frappe.log_error(title="API GET Failure", message=f"Failed to fetch driver data. Status code: {get_response.status_code}, Response: {get_response.text}")
        else:
            frappe.log_error(title="API PUT Failure", message=f"Failed to update driver status. Status code: {put_response.status_code}, Response: {put_response.text}")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(title="API Exception", message=f"An error occurred while communicating with the external API: {e}")


def post_service_request_to_external_api(doc, method):
    # Define the API endpoints
    post_api_url = "http://195.200.14.68/hlf/service-request/create"
    get_api_url = f"http://195.200.14.68/hlf/service-request/get/{doc.name}"
    
    # Prepare the data to be sent to the external API
    service_request_data = {
        "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
        "customerId": doc.customer,
        "driverId": doc.assigned_to_driver,
        "vehicleId": doc.assigned_to_vehicle,
        "hubId": doc.hub,
        "ServiceRequestId": doc.name,
        "servicePartnerId": "sp345",
        "destinationLongitude": doc.destination_longitude,
        "destinationLatitude": doc.destination_latitude,
        "status": doc.status,  # Assuming all new customers are active
        "modifiedBy": frappe.session.user,
        "createdBy": doc.owner,
        "createdDateTime": now().split(" ")[0],  # Current date in "YYYY-MM-DD" format
        "modifiedDate": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format
    }
    
    try:
        # Send the POST request
        post_response = requests.post(post_api_url, data=json.dumps(service_request_data), headers={'Content-Type': 'application/json'})
        
        # Log the response details
        # frappe.log_error(f"POST Response Status Code: {post_response.status_code}", "API POST Response Status Code")
        # frappe.log_error(f"POST Response Text: {post_response.text}", "API POST Response Text")
        
        # Check for a successful response
        if post_response.status_code == 200:
            frappe.log_error("service-request data posted successfully to the external API.", "API POST Success")
            frappe.msgprint("service-request data posted successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            
            # frappe.log_error(f"GET Response Text: {get_response.text}", "API GET Response Text")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Service Request",doc.name,"validation",json.dumps(external_data))
                # doc.custom_validation = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                
                frappe.msgprint("service-request data fetched and updated successfully from the external API.", "API GET Success")
            else:
                frappe.log_error(f"Failed to fetch service-request data. Status code: {get_response.status_code}, Response: {get_response.text}", "API GET Failure")
        else:
            frappe.log_error(f"Failed to post service-request data. Status code: {post_response.status_code}, Response: {post_response.text}", "API POST Failure")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"An error occurred while communicating with the external API: {e}", "API Exception")

def update_service_request_status_and_fetch_data(doc, method):
    # Define the API endpoints
    # stats=[]
    # if doc.disabled==1:
    #     stats.append("Disabled")
    # else:
    #     stats.append("Enabled")
    put_api_url = "http://195.200.14.68/hlf/service-request/update-status"
    get_api_url = f"http://195.200.14.68/hlf/service-request/get/{doc.name}"
    
    try:
        # Prepare data for the PUT request to update the status
        update_data = {
            "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
            "status": doc.status , # Modify the status as needed
            "modifiedBy": frappe.session.user,
            "modifiedDate": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format

        }
        
        # Send the PUT request to update the status
        put_response = requests.put(put_api_url, data=json.dumps(update_data), headers={'Content-Type': 'application/json'})
        
        # Log the PUT response details
        # frappe.log_error(title="API PUT Response Status Code", message=f"PUT Response Status Code: {put_response.status_code}")
        # frappe.log_error(title="API PUT Response Text", message=f"PUT Response Text: {put_response.text}")
        
        # Check for a successful PUT response
        if put_response.status_code == 200:
            # frappe.log_error(title="API PUT Success", message="Customer status updated successfully in the external API.")
            frappe.msgprint("service-request data updated successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            # frappe.log_error(title="API GET Response Status Code", message=f"GET Response Status Code: {get_response.status_code}")
            # frappe.log_error(title="API GET Response Text", message=f"GET Response Text: {get_response.text}")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Service Request",doc.name,"validation",json.dumps(external_data))
                # doc.external_api_data = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                # frappe.log_error(title="API GET Success", message="Customer data fetched and updated successfully from the external API.")
                frappe.msgprint("service-request data pulled successfully to the external API.", "API POST Success")
            else:
                frappe.log_error(title="API GET Failure", message=f"Failed to fetch service-request data. Status code: {get_response.status_code}, Response: {get_response.text}")
        else:
            frappe.log_error(title="API PUT Failure", message=f"Failed to update service-request status. Status code: {put_response.status_code}, Response: {put_response.text}")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(title="API Exception", message=f"An error occurred while communicating with the external API: {e}")


def post_vehicle_to_external_api(doc, method):
    # Define the API endpoints
    post_api_url = "http://195.200.14.68/hlf/vehicle/create"
    get_api_url = f"http://195.200.14.68/hlf/vehicle/get/{doc.name}"
    
    # Prepare the data to be sent to the external API
    vehicle_data = {
        "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
        "licenseplate": doc.license_plate,
        "model": doc.model,
        "make": doc.make,
        "odometervalue":doc.last_odometer,
        "chasisno": doc.chassis_no,
        "status": doc.custom_status,  # Assuming all new customers are active
        "modifiedBy": frappe.session.user,
        "createdBy": doc.owner,
        "createdDateTime": now().split(" ")[0],  # Current date in "YYYY-MM-DD" format
        "modifiedDate": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format
    }
    
    try:
        # Send the POST request
        post_response = requests.post(post_api_url, data=json.dumps(vehicle_data), headers={'Content-Type': 'application/json'})
        
        # Log the response details
        # frappe.log_error(f"POST Response Status Code: {post_response.status_code}", "API POST Response Status Code")
        # frappe.log_error(f"POST Response Text: {post_response.text}", "API POST Response Text")
        
        # Check for a successful response
        if post_response.status_code == 200:
            frappe.log_error("service-request data posted successfully to the external API.", "API POST Success")
            frappe.msgprint("service-request data posted successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            
            # frappe.log_error(f"GET Response Text: {get_response.text}", "API GET Response Text")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Vehicle",doc.name,"custom_validation",json.dumps(external_data))
                # doc.custom_validation = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                
                frappe.msgprint("service-request data fetched and updated successfully from the external API.", "API GET Success")
            else:
                frappe.log_error(f"Failed to fetch service-request data. Status code: {get_response.status_code}, Response: {get_response.text}", "API GET Failure")
        else:
            frappe.msgprint("Error")
            # frappe.log_error(f"Failed to post service-request data. Status code: {post_response.status_code}, Response: {post_response.text}", "API POST Failure")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"An error occurred while communicating with the external API: {e}", "API Exception")

def update_vehicle_status_and_fetch_data(doc, method):
    # Define the API endpoints
    # stats=[]
    # if doc.disabled==1:
    #     stats.append("Disabled")
    # else:
    #     stats.append("Enabled")
    put_api_url = "http://195.200.14.68/hlf/vehicle/update-status"
    get_api_url = f"http://195.200.14.68/hlf/vehicle/get/{doc.name}"
    
    try:
        # Prepare data for the PUT request to update the status
        update_data = {
            "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
            "status": doc.custom_status 
        }
        
        # Send the PUT request to update the status
        put_response = requests.put(put_api_url, data=json.dumps(update_data), headers={'Content-Type': 'application/json'})
        
        # Log the PUT response details
        # frappe.log_error(title="API PUT Response Status Code", message=f"PUT Response Status Code: {put_response.status_code}")
        # frappe.log_error(title="API PUT Response Text", message=f"PUT Response Text: {put_response.text}")
        
        # Check for a successful PUT response
        if put_response.status_code == 200:
            # frappe.log_error(title="API PUT Success", message="Customer status updated successfully in the external API.")
            frappe.msgprint("service-request data updated successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            # frappe.log_error(title="API GET Response Status Code", message=f"GET Response Status Code: {get_response.status_code}")
            # frappe.log_error(title="API GET Response Text", message=f"GET Response Text: {get_response.text}")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Vehicle",doc.name,"custom_validation",json.dumps(external_data))
                # doc.external_api_data = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                # frappe.log_error(title="API GET Success", message="Customer data fetched and updated successfully from the external API.")
                frappe.msgprint("service-request data pulled successfully to the external API.", "API POST Success")
            else:
                frappe.log_error(title="API GET Failure", message=f"Failed to fetch service-request data. Status code: {get_response.status_code}, Response: {get_response.text}")
        else:
            frappe.log_error(title="API PUT Failure", message=f"Failed to update service-request status. Status code: {put_response.status_code}, Response: {put_response.text}")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(title="API Exception", message=f"An error occurred while communicating with the external API: {e}")


def post_vehiclea_to_external_api(doc, method):
    # Define the API endpoints
    post_api_url = "http://195.200.14.68/hlf/vehicle-assignment/create"
    get_api_url = f"http://195.200.14.68/hlf/vehicle-assignment/get/{doc.name}"
    
    # Prepare the data to be sent to the external API
    vehicle_data = {
        "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
        "vehicleId": doc.vehicle,
        "assignDate": now().split(" ")[0],
        "pickDatetime": doc.pick_time,
        "dropDatetime": doc.drop_time,
        "status": "Active",  # Assuming all new customers are active
        "modifiedBy": frappe.session.user,
        "createdBy": doc.owner,
        "createdDateTime": now().split(" ")[0],  # Current date in "YYYY-MM-DD" format
        "modifiedDate": now().split(" ")[0]  # Current date in "YYYY-MM-DD" format
    }
    
    try:
        # Send the POST request
        post_response = requests.post(post_api_url, data=json.dumps(vehicle_data), headers={'Content-Type': 'application/json'})
        
        # Log the response details
        # frappe.log_error(f"POST Response Status Code: {post_response.status_code}", "API POST Response Status Code")
        # frappe.log_error(f"POST Response Text: {post_response.text}", "API POST Response Text")
        
        # Check for a successful response
        if post_response.status_code == 200:
            frappe.log_error("vehicle-assignment data posted successfully to the external API.", "API POST Success")
            frappe.msgprint("vehicle-assignment data posted successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            
            # frappe.log_error(f"GET Response Text: {get_response.text}", "API GET Response Text")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Vehicle Assignment",doc.name,"validation",json.dumps(external_data))
                # doc.custom_validation = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                
                frappe.msgprint("vehicle-assignment data fetched and updated successfully from the external API.", "API GET Success")
            else:
                frappe.log_error(f"Failed to fetch vehicle-assignment data. Status code: {get_response.status_code}, Response: {get_response.text}", "API GET Failure")
        else:
            frappe.log_error(f"Failed to post vehicle-assignment data. Status code: {post_response.status_code}, Response: {post_response.text}", "API POST Failure")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"An error occurred while communicating with the external API: {e}", "API Exception")

def update_vehiclea_status_and_fetch_data(doc, method):
    # Define the API endpoints
    # stats=[]
    # if doc.disabled==1:
    #     stats.append("Disabled")
    # else:
    #     stats.append("Enabled")
    put_api_url = "http://195.200.14.68/hlf/vehicle-assignment/update-status"
    get_api_url = f"http://195.200.14.68/hlf/vehicle-assignment/get/{doc.name}"
    
    try:
        # Prepare data for the PUT request to update the status
        update_data = {
            "id": doc.name,  # Assuming 'name' is the unique ID in ERPNext
            "status": "Active" 
        }
        
        # Send the PUT request to update the status
        put_response = requests.put(put_api_url, data=json.dumps(update_data), headers={'Content-Type': 'application/json'})
        
        # Log the PUT response details
        # frappe.log_error(title="API PUT Response Status Code", message=f"PUT Response Status Code: {put_response.status_code}")
        # frappe.log_error(title="API PUT Response Text", message=f"PUT Response Text: {put_response.text}")
        
        # Check for a successful PUT response
        if put_response.status_code == 200:
            # frappe.log_error(title="API PUT Success", message="Customer status updated successfully in the external API.")
            frappe.msgprint("vehicle-assignment data updated successfully to the external API.", "API POST Success")
            
            # Send the GET request to fetch the updated data
            get_response = requests.get(get_api_url)
            
            # Log the GET response details
            # frappe.log_error(title="API GET Response Status Code", message=f"GET Response Status Code: {get_response.status_code}")
            # frappe.log_error(title="API GET Response Text", message=f"GET Response Text: {get_response.text}")
            
            # Check for a successful GET response
            if get_response.status_code == 200:
                # Parse the JSON response
                external_data = get_response.json()
                
                # Update the customer document in ERPNext with the fetched data
                frappe.db.set_value("Vehicle Assignment",doc.name,"validation",json.dumps(external_data))
                # doc.external_api_data = json.dumps(external_data)
                # doc.save(ignore_permissions=True)
                
                # frappe.log_error(title="API GET Success", message="Customer data fetched and updated successfully from the external API.")
                frappe.msgprint("vehicle-assignment data pulled successfully to the external API.", "API POST Success")
            else:
                frappe.log_error(title="API GET Failure", message=f"Failed to fetch vehicle-assignment data. Status code: {get_response.status_code}, Response: {get_response.text}")
        else:
            frappe.log_error(title="API PUT Failure", message=f"Failed to update vehicle-assignment status. Status code: {put_response.status_code}, Response: {put_response.text}")
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(title="API Exception", message=f"An error occurred while communicating with the external API: {e}")


@frappe.whitelist()
def send_data_to_optimize_route(doc, method="None"):
    # doc=frappe.get_doc("Shipment Delivery",docsname)
    # Prepare the data
    # source_location = {
    #     "latitude": float(doc.pickup_latitude),
    #     "longitude": float(doc.pickup_longitude)
    # }
    # source_location= {
    #     "latitude": 33.30890574,
    #     "longitude": 44.4279963
    # }
    
    destination_latitudes = []
    destination_longitudes=[]
    sr=[]
    data1 = {
        "source_latitude": float(doc.pickup_latitude),
        "source_longitude": float(doc.pickup_longitude),
        "destination_latitudes": destination_latitudes,
        "destination_longitudes":destination_longitudes,
        "service_request": sr
    }
    # Headers
    headers1 = {
        "Authorization": "token 2ded6868a0946dd:22b9bff0aeaf4a8"
    }

    for child in doc.get("delivery_stops"):
        destination_latitudes.append(float(child.latitude))
        destination_longitudes.append(float(child.longitude))
        sr.append(child.service_request)
        # post_response1 = requests.get("http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api", json=data1, headers=headers1)
        # api_response1=post_response1.json()
        # frappe.db.set_value("Delivery Stops",doc.name,"route_data1", json.dumps(post_response1.json()))
    # destination_locations=[
    #     {
    #         "latitude": 39.36884572,
    #         "longitude": 44.27144632
    #     },
    # ]
    
    data = {
        "source_latitude": float(doc.pickup_latitude),
        "source_longitude": float(doc.pickup_longitude),
        "destination_latitudes": destination_latitudes,
        "destination_longitudes":destination_longitudes,
        "service_request": sr
    }
    # Headers
    headers = {
        "Authorization": "token 2ded6868a0946dd:22b9bff0aeaf4a8"
    }
    # Make the POST request
    post_response = requests.get("http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api", json=data, headers=headers)
    # response = requests.post("https://optimize-route-21.onrender.com/optimize_route", json=data)
    
    # Handle the response
    # frappe.msgprint(destination_locations)
    frappe.log_error(title="API GET Failure", message=f"route to fetch vehicle-assignment data. Status code: {post_response.status_code}, Response: {destination_latitudes}")
    if post_response.status_code == 200:
        api_response=post_response.json()
        frappe.log_error(title="API GET Failure", message=f"route to fetch vehicle-assignment data. Status code: {post_response.status_code}, Response: {json.dumps(post_response.json())}")
        # frappe.db.set_value("Shipment Delivery1",doc.name,"mhtml", json.dumps(post_response.json()))
        doc.route_data1= json.dumps(post_response.json())
        # doc.save()
        frappe.msgprint("Succesfully Optimized")
        # sorted_service_requests = []
        # message = api_response.get("message", {})
        # route_info_google = message.get("route_info_google", {})
        # route_info_mapbox = message.get("route_info_mapbox", {})
        # if route_info_google:
        #     for route_info in route_info_google.get("route_info", []):
        #         route_dict = {item[0]: item[1] for item in route_info}
        #         distance = route_info.get("distance")
        #         distance_value = distance.split()[0]  
        #         for service_request in sr:
        #             if route_info.get("destination").get("latitude") == service_request.get("latitude") and route_info.get("destination").get("longitude") == service_request.get("longitude"):
        #                 sorted_service_requests.append({
        #                     "service_request": service_request,
        #                     "distance": float(distance_value)
        #                 })
        #     sorted_service_requests.sort(key=lambda x: float(x.get("distance")), reverse=False)
        #     for child, sorted_sr in zip(doc.get("delivery_stops"), sorted_service_requests):
        #         child.set("distance", sorted_sr.get("distance"))
        #         child.set("service_request", sorted_sr.get("service_request"))
        #         child.save()
        #     # doc.route_data = response.json()
        #     # doc.save()
        #     # frappe.db.commit()
        #     return sorted_service_requests
        # else:
        #     frappe.throw("Failed to get the optimized route")

        # if route_info_mapbox:
        #     for route_info in message.get("route_info_mapbox").get("route_info"):
        #         distance = route_info.get("distance")
        #         distance_value = distance.split()[0]  
        #         for service_request in destination_locations:
        #             if route_info.get("destination").get("latitude") == service_request.get("latitude") and route_info.get("destination").get("longitude") == service_request.get("longitude"):
        #                 sorted_service_requests.append({
        #                     "service_request": service_request.get("service_request"),
        #                     "distance": float(distance_value)
        #                 })
        #     sorted_service_requests.sort(key=lambda x: float(x.get("distance")), reverse=False)
        #     for child, sorted_sr in zip(doc.get("delivery_stops"), sorted_service_requests):
        #         child.set("distance", sorted_sr.get("distance"))
        #         child.set("service_request", sorted_sr.get("service_request"))
        #         child.save()
        #     # doc.route_data = response.json()
        #     # doc.save()
        #     # frappe.db.commit()
        #     return sorted_service_requests
        # else:
        #     frappe.throw("Failed to get the optimized route")

@frappe.whitelist()
def get_item_code_by_barcode(barcode):
    try:
        # Query to fetch item details based on barcode
        item = frappe.get_all('Service Request', 
                              filters={'name': barcode}, 
                              fields=['name', 'destination_latitude', 'destination_longitude','request_date','custom_plot_number',"custom_neighborhood1","custom_areas"])
        if item:
            return item
        else:
            frappe.msgprint(__('Item not found'))
            return []
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Error in get_item_code_by_barcode for barcode {barcode}")
        return frappe.throw(_("Unable to fetch item details"))

@frappe.whitelist()
def send_data_to_optimize_routechild(docsname, dcc="None"):
    doc = frappe.get_doc("Shipment Delivery", docsname)
    
    # Prepare common data
    source_latitude = float(doc.pickup_latitude)
    source_longitude = float(doc.pickup_longitude)

    headers = {
        "Authorization": "token 2ded6868a0946dd:22b9bff0aeaf4a8"
    }

    for child in doc.get("delivery_stops"):
        destination_latitude = float(child.latitude)
        destination_longitude = float(child.longitude)
        service_request = child.service_request
        
        data = {
            "source_latitude": source_latitude,
            "source_longitude": source_longitude,
            "destination_latitudes": [destination_latitude],
            "destination_longitudes": [destination_longitude],
            "service_request": [service_request]
        }
        
        # Make the GET request
        post_response = requests.get("http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api", json=data, headers=headers)
        
        if post_response.status_code == 200:
            api_response = post_response.json()
            frappe.msgprint(f"Successfully optimized for Delivery Stop {child.name}")
            
            # Update the `route_data` field in the `Delivery Stops` child table
            frappe.db.set_value("Delivery Stops", child.name, "route_data", json.dumps(api_response))
            frappe.db.commit()
        else:
            frappe.log_error(title="API GET Failure", message=f"Failed to fetch route data for Delivery Stop {child.name}. Status code: {post_response.status_code}, Response: {post_response.text}")
            frappe.msgprint(f"Failed to optimize for Delivery Stop {child.name}")

    # Optionally, update the `route_data` field in the `Shipment Delivery` doctype with overall data if needed
    overall_data = {
        "source_latitude": source_latitude,
        "source_longitude": source_longitude,
        "destination_latitudes": [float(child.latitude) for child in doc.get("delivery_stops")],
        "destination_longitudes": [float(child.longitude) for child in doc.get("delivery_stops")],
        "service_request": [child.service_request for child in doc.get("delivery_stops")]
    }
    overall_response = requests.get("http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api", json=overall_data, headers=headers)
    
    if overall_response.status_code == 200:
        overall_api_response = overall_response.json()
        frappe.db.set_value("Shipment Delivery", doc.name, "route_data1", json.dumps(overall_api_response))
        frappe.db.commit()
        frappe.msgprint(f"Successfully optimized overall route data {docsname}")
    else:
        frappe.log_error(title="API GET Failure", message=f"Failed to fetch overall route data. Status code: {overall_response.status_code}, Response: {overall_response.text}")
        frappe.msgprint("Failed to optimize overall route data")


@frappe.whitelist()
def send_data_to_optimize_routechild1(docsname, Methods="None"):
    doc = frappe.get_doc("Shipment Delivery", docsname)
    
    # Prepare common data
    source_latitude = float(doc.pickup_latitude)
    source_longitude = float(doc.pickup_longitude)

    headers = {
        "Authorization": "token 2ded6868a0946dd:22b9bff0aeaf4a8"
    }

    for child in doc.get("delivery_stops"):
        destination_latitude = float(child.latitude)
        destination_longitude = float(child.longitude)
        service_request = child.service_request
        
        data = {
            "source_latitude": source_latitude,
            "source_longitude": source_longitude,
            "destination_latitudes": [destination_latitude],
            "destination_longitudes": [destination_longitude],
            "service_request": [service_request]
        }
        
        # Make the GET request
        post_response = requests.get("http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api", json=data, headers=headers)
        
        if post_response.status_code == 200:
            api_response = post_response.json()
            frappe.msgprint(f"Successfully optimized for Delivery Stop {child.name}")
            
            # Update the `route_data` field in the `Delivery Stops` child table
            child.route_data = json.dumps(api_response)
        else:
            frappe.log_error(title="API GET Failure", message=f"Failed to fetch route data for Delivery Stop {child.name}. Status code: {post_response.status_code}, Response: {post_response.text}")
            frappe.msgprint(f"Failed to optimize for Delivery Stop {child.name}")

    # Save the changes to the child table
    # doc.save()
    
    # Optionally, update the `route_data` field in the `Shipment Delivery` doctype with overall data if needed
    overall_data = {
        "source_latitude": source_latitude,
        "source_longitude": source_longitude,
        "destination_latitudes": [float(child.latitude) for child in doc.get("delivery_stops")],
        "destination_longitudes": [float(child.longitude) for child in doc.get("delivery_stops")],
        "service_request": [child.service_request for child in doc.get("delivery_stops")]
    }
    overall_response = requests.get("http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api", json=overall_data, headers=headers)
    
    if overall_response.status_code == 200:
        overall_api_response = overall_response.json()
        doc.route_data1 = json.dumps(overall_api_response)
        frappe.msgprint("Successfully optimized overall route data")
    else:
        frappe.log_error(title="API GET Failure", message=f"Failed to fetch overall route data. Status code: {overall_response.status_code}, Response: {overall_response.text}")
        frappe.msgprint("Failed to optimize overall route data")
    
    # Save the changes to the parent document
    doc.save()


@frappe.whitelist()
def fetch_vehicle_assignment_data():
    docsname="IPSD240617001"
    api_url = "http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api"
    doc=frappe.get_doc("Shipment Delivery",docsname)
    # Prepare the data
    # source_latitude = {
    #     "latitude": float(doc.pickup_latitude),
    #     "longitude": float(doc.pickup_longitude)
    # }
    # source_location= {
    #     "latitude": 33.30890574,
    #     "longitude": 44.4279963
    # }
    
    destination_latitudes = []
    destination_longitudes=[]

    for child in doc.get("delivery_stops"):
        destination_latitudes.append(float(child.latitude))
        destination_longitudes.append(float(child.longitude))
        # destination_locations.append({
        #     "latitude": float(child.latitude),
        #     "longitude": float(child.longitude),
        #     "service_request":child.service_request
        # })
    # destination_locations=[
    #     {
    #         "latitude": 39.36884572,
    #         "longitude": 44.27144632
    #     },
    # ]
    
    data = {
        "source_latitude": float(doc.pickup_latitude),
        "source_longitude": float(doc.pickup_longitude),
        "destination_latitudes": destination_latitudes,
        "destination_longitudes":destination_longitudes
    }
    # Headers
    headers = {
        "Authorization": "token 2ded6868a0946dd:22b9bff0aeaf4a8"
    }
    try:
        response = requests.get(api_url, headers=headers,json=data)

        # Check if the request was successful
        if response.status_code == 200:
            print("API call successful")
            overall_api_response = response.json()
            frappe.db.set_value("Shipment Delivery", doc.name, "route_data1", json.dumps(overall_api_response))
            frappe.db.commit()
            return response.json()  # Return the response data
        else:
            return f"API call failed with status code {response.status_code}. Response: {response.text}"
    
    except requests.RequestException as e:
        return f"An error occurred: {e}"


@frappe.whitelist()
def notify_issue_creation(doc, method):
    # This function will be called when an Issue is created
    message = f"{frappe.session.user} just created an {doc.subject}..."
    # Publish the real-time message to the Administrator user
    frappe.publish_realtime(event='msgprint', message=message, user=doc.for_user)


@frappe.whitelist(allow_guest=True)
def send_sms_customer(doc,method=None):
    message = "Thank you for registering with Tasheel. Please download our app from the link below to manage your address."
    if doc.custom_mobile:
        url = "https://gateway.standingtech.com/api/v4/sms/send"
        payload = {
            "recipient": doc.custom_mobile,
            "sender_id": "AtlasGisIT",
            "type": "sms",
            "message": message,
            "lang": "en"
        }
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer 212|niaOrZ6mtE0eXio2lih4bFgxaE0T5Kmn9PqmoecD1f2332d9",
            'Content-Type': "application/json"
        }
        
       
        response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            
        if response.status_code == 200:
            response_data = response.json()
            frappe.msgprint("Sucessfuly Sent")    
        else:
            frappe.log_error(f"Failed to send OTP. Status Code: {response.status_code}, Response: {response.text}")
            frappe.msgprint("Sucessfuly Not Sent")

