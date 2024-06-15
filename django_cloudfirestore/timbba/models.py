"""
    This module contains Django models for the the Client ,Roles ,User ,UserRole ,Consignment ,Log.
"""

from django.db import models

class Roles(models.Model):
    """
        A Django model to create roles table in database with following field.

        Attributes:
            id : it is generated automatically .It uniquely identifies each role in database table
            name:Name of a role in database table.
        
        Method:
            role_serializer(): Returns a dictionary containing serialized role data.

    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

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

class Client(models.Model):
    """
        A Django model to create client tables in database.it stores client related data.

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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=20) 
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    def client_serializer(self, include_fields=None):
            return {
                'id': self.id,
                'name': self.name,
                'address': self.address,
                'contact': self.contact,
                'updated_at': self.updated_at,
                'created_at': self.created_at,
                'email': self.email,
            }

class User(models.Model):
    """
        User model to create table in database and stores user's information and role associated with each user.

        Attributes:
            id: it is generated automatically .It uniquely identifies each user in database table.
            name: name of the client.
            username : it is unique for each user ,We require username when login to the application.
            role:  each user will have role ,for example a user can access applicaiton using web or mobile or both.
            contact :phone number of a user so that we can contact when we need.
            client: each user will be belonging to a particular client.
            updated_at: last updated date of user information in database table.
            created_date: Date of current user creation in database table.
        
        Method:
            user_serializer(): returns dictionary of user information with key-value pair.

    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def user_serializer(self):
        role_data = self.role.id  if self.role else None
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


class UserRole(models.Model):
    """
        This model creates table in database and stores information of roles of each user .
        For example if user has role web so this table will have id of role and with user information.

        Attributes:
            id: it is generated automatically .It uniquely identifies each column in database table.
            user : it also stores user id to indicate that this role is of this particular user.
            role : id of the role which is provided to the current user.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)


class Consignment(models.Model):
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
    TYPE_CHOICES = (
        ('Type1', 'Type 1'),
        ('Type2', 'Type 2'),
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_consignments')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_consignments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def con_serializer(self):
        client_id = self.client_id.id if self.client_id else None
        user_id = self.created_by.id if self.created_by else None

        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'client_id': client_id,
            'created_by':user_id,
            'updated_by': user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class Item(models.Model):
    """
        Model creates table to store information of a log.

        Attributes:
            consignment: each log belongs to a particular consignment so each log will have consignment id.
            barcode: each log has barcode to uniquely identify each log.
            length : dimension of log (height of of log)
            volume : volume of log.

        Method:
            log_serializer(): returns dictionary of log information with key value pair.with consignment

    """
    consignment = models.ForeignKey(Consignment, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    def log_serializer(self):
        con_id = self.consignment.id if self.consignment else None
        return {
            'consignment_id': con_id,
            'barcode': self.barcode,
            'length': self.length,
            'volume': self.volume
        }
    
