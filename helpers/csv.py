from csv import writer

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='', encoding="utf-8") as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
    print('Data saved successfully!')

def export_to_csv(user, phone, filename='accounts.csv'):
    mail_id = user['username'] + '@gmail.com'
    account = {
        "username": mail_id,
        "password": user['password'],
        "firstname": user['firstname'],
        "lastname": user['lastname'],
        "phone": phone['phone']
    }
    genders = ['Male', 'Female', 'Rather not to say']
    g_index = int(user['gender']) - 1
    gender = genders[g_index]
    account['gender'] = gender
    dob = str(user['dob']['day']) + '/' + str(user['dob']['month']) + '/' + str(user['dob']['year']) 
    account['dob']  = dob
    values = account.values()
    values_list = list(values)
    append_list_as_row(filename, values_list)