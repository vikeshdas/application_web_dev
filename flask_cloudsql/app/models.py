
"""
    This module contains Flask models for the the Client ,Roles ,User ,UserRole ,Consignment ,Log.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Roles(db.Model):
    """
        A Flask model to create roles table in database with following field.

        Attributes:
            id : it is generated automatically .It uniquely identifies each role in database table
            name:Name of a role in database table.
        
        Method:
            role_serializer(): Returns a dictionary containing serialized role data.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def role_serializer(self):
        """
            Convert role object into dictionary.This function takes role object and convert into dictionary
            with id of role and name of role.

            Return: Return A dictionary representing the serialized role object.
        """
        return {
            'id': self.id,
            'name': self.name,
        }

class Client(db.Model):
    """
        A Flask model to create client tables in database.it stores client related data.

        Attributes:
            id: it is generated automatically .It uniquely identifies each client in database table.
            name: Name of client.
            address: Home address of a client. proper address with city,state,country, zip.
            contact: A phone number to contact client.
            updated_at: last updated date of client information in database table.
            created_date: Date of client creation in database table.

        Methods:
            client_serializer(): returns dictionary of client information with key value pair.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.Text)
    contact = db.Column(db.String(20))
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    email = db.Column(db.String(120))

    def client_serializer(self, include_fields=None):
        """
            Convert client object into dictionary.This function takes client object and convert into dictionary
            with id, name , address ,contact,updated_at,created_at,email of the client.

            Return: Return A dictionary representing the serialized client object.
        """
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'contact': self.contact,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
            'email': self.email,
        }

class User(db.Model):
    """
        User model to create table in database and stores user's information and role associated with each user.

        Attributes:
            id: it is generated automatically .It uniquely identifies each user in database table.
            name: name of the client.
            username : it is unique for each user ,We require username when login to the application.
            role:  each user will have role ,for example a user can access application using web or mobile or both.
            contact :phone number of a user so that we can contact when we need.
            client: each user will be belonging to a particular client.
            updated_at: last updated date of user information in database table.
            created_date: Date of current user creation in database table.
        
        Method:
            user_serializer(): returns dictionary of user information with key-value pair.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    contact = db.Column(db.String(20))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    role = db.relationship('Roles', backref='users')
    client = db.relationship('Client', backref='users')

    def user_serializer(self):
        """
            Convert user object into dictionary.This function takes user's object and convert into dictionary
            with role's object,client's object, id , name ,username,role_id,contact, created_at,updated_at of the client.

            Return: Return A dictionary representing the serialized user object.
        """
                
        role_data = self.role.id if self.role else None
        client_id = self.client.id if self.client else None

        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'role_id': role_data,
            'contact': self.contact,
            'client_id': client_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class UserRole(db.Model):
    """
        This model creates table in database and stores information of roles of each user .
        For example if user has role web so this table will have id of role and with user information.

        Attributes:
            id: it is generated automatically .It uniquely identifies each column in database table.
            user : it also stores user id to indicate that this role is of this particular user.
            role : id of the role which is provided to the current user.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

class Consignment(db.Model):
    """
        This model creates table for consignment.Each consignment 
        will have more than one log with log's dimensions.

        Attributes:
            id: it is generated automatically .It uniquely identifies each column in database table.
            name : name of the consignment.
            type:  type of consignment.There is two type of consignment hardwood and pinewood.
            client_id: Each consignment will be belonging to a particular client.
            updated_at: last updated date of consignment information in database table.
            created_date: Date of current consignment's creation in database table.

            Method:
                user_serializer(): returns dictionary of consignment information with key value pair.with client information

    """
    TYPE_CHOICES = [
        ('Type1', 'Type 1'),
        ('Type2', 'Type 2'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(20), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    client = db.relationship('Client', backref='consignments')
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_consignments')
    updated_by = db.relationship('User', foreign_keys=[updated_by_id], backref='updated_consignments')

    def con_serializer(self):
        """
            Convert Consignment's object into dictionary.This function takes Consignments's object and convert into dictionary
            with  id , name ,type,client_id,created_by,updated_by created_at,updated_at of the client.

            Return: Return A dictionary representing the serialized user object.
        """
        client_id = self.client_id if self.client_id else None
        created_by_id = self.created_by_id if self.created_by_id else None

        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'client_id': client_id,
            'created_by': created_by_id,
            'updated_by': self.updated_by_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class Logs(db.Model):
    """
        Model creates table to store information of a log.

        Attributes:
            consignment: each log belongs to a particular consignment so each log will have consignment id.
            barcode: each log has barcode to uniquely identify each log.
            length : dimension of log (height of the log)
            volume : volume of log.

        Method:
            log_serializer(): returns dictionary of log information with key value pair.with consignment

    """
    id = db.Column(db.Integer, primary_key=True)
    consignment_id = db.Column(db.Integer, db.ForeignKey('consignment.id'))
    barcode = db.Column(db.String(50))
    length = db.Column(db.Float(precision=2))
    volume = db.Column(db.Float(precision=2))

    def log_serializer(self):
        """
            Convert Logs's object into dictionary.This function takes Logs's object and convert into dictionary
            with  consignment_id , barcode ,length,volume of the log.

            Return: Return A dictionary representing the serialized log object.
        """
        consignment_id = self.consignment_id if self.consignment_id else None
        return {
            'consignment_id': consignment_id,
            'barcode': self.barcode,
            'length': self.length,
            'volume': self.volume
        }


