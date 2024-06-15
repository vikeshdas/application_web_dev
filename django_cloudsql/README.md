## Django
I used the VIEW class of Django which provides features to create a view including request , response handling, and error handling , database is used to store the data.ORM feature is used to design the database schema. Defined a model Django models are Python classes that represents database tables. Each model class corresponds to a table, and the class attributes define the table's fields.

## ORM
I have used Django's object relation maping in my project. ORM is a way to interact with database using classes. We can create class, object and use them to interact with database instead of writing naked DB queries.

For example:
```
class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
```

- we created a class Roles, above class will create table in database

- if we want to insert data in above table then we don't need to write database query. Instead we will create object of the above class, mention below.

- new_obj=Roles(name="web");

- Then new_obj.save() ->this function will save above entry in Roles table.

- So as you can see I created Database table , inserted data in table using object oriented.
