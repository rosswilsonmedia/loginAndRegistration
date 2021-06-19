from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM users WHERE id=%(id)s;"
        result=connectToMySQL('login_and_registration_schema').query_db(query, data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        result=connectToMySQL('login_and_registration_schema').query_db(query, data)
        print(result)
        if len(result)<1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query="INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)"\
            "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        result=connectToMySQL('login_and_registration_schema').query_db(query, data)
        return result

    @staticmethod
    def validate(data):
        is_valid=True
        if len(data['first_name'])<2:
            flash('*First name must be at least two characters', 'register_errors')
            is_valid=False

        if len(data['last_name'])<2:
            flash('*Last name must be at least two characters', 'register_errors')
            is_valid=False

        if not EMAIL_REGEX.match(data['email']):
            flash('*Invalid email address', 'register_errors')
            is_valid=False
        elif User.check_duplicate(data):
            flash(f"*{data['email']} is already in use on this site", 'register_errors')
            is_valid=False

        if len(data['password'])<8:
            flash('*Passwords must be at least eight characters', 'register_errors')
            is_valid=False
        elif data['password']!=data['confirm_password']:
            flash('*Passwords do not match', 'errors')
            is_valid=False

        return is_valid


    @staticmethod
    def check_duplicate(data):
        query='SELECT * FROM emails WHERE email=%(email)s;'
        results=connectToMySQL('email_validation_schema').query_db(query, data)
        print(len(results))
        is_dup=False
        if len(results)>0:
            is_dup=True
        return is_dup