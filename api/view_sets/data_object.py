from rest_framework.exceptions import APIException


class DataObjects():
    def user_data(data):
        user = {}
        user['first_name'] = data['first_name']
        user['last_name'] = data['last_name']
        user['email'] = data['email']
        user['is_active'] = 1
        if 'username' in data:
            user['username'] = data['username']
        else:
            user['username'] = data['email']
        return user

    def client_data(data):
        client = {}
        client['postal_address'] = data['postal_address']
        client['phone_number'] = data['phone_number']
        return client

    def profile_data(data):
        profile = {}
        profile['phone_number'] = data['phone_number']
        return profile
