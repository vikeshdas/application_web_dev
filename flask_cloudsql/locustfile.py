from locust import HttpUser, task
import json
import random

created_user=[1]
created_client=[1]
created_consignment=[1]
created_log=[1]
user_names_list = ["Frank", "Grace", "Hannah", "Isaac", "Jack", "Kelly", "Liam", "Mia", "Nathan", "Olivia",
                    "Paul", "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xander", "Yara",
                    "Zoe", "Adam", "Ben", "Chloe", "Daisy", "Ethan", "Fiona", "George", "Holly", "Ian", "Jenny",
                    "Kevin", "Lucy", "Mike", "Nancy", "Oscar", "Penny", "Quincy", "Ruth", "Simon", "Tanya",
                    "Ulysses", "Violet", "William", "Xavier", "Yvonne", "Zack","vikesh","dheeraj","rahul","gopla"]
"""
    Python class for performance testing.
"""
class HelloWorldUser(HttpUser):

    @task
    def create_user(self):
        global created_user
        global created_client
        global user_names_list
        client_id = created_client[random.randint(0, len(created_client)-1)]
        name=user_names_list[random.randint(0, 49)]
        contact ="+91 " + "".join([str(random.randint(0, 9)) for _ in range(10)])
        response=self.client.put("http://backend_service:8000/user", json={"client_id":1,"name":name,"username":"user"+name,"contact":contact,"role_id":3,"address": "delhi"})
        if response.status_code == 200 or response.status_code==201 :                         
            response_data = json.loads(response.text)
            created_user.append(response_data)
            print("user",created_user)
        else:
            response_data = json.loads(response.text)
            print("PUT user request failed with status code:", response_data)

    @task
    def get_user(self):
        global created_user
        if len(created_user)>=1:
            user=created_user[random.randint(0, len(created_user)-1)]
            response=self.client.get("http://backend_service:8000/user", json={ "user_id":2})
            if response.status_code == 200 or response.status_code == 201 :
                response_data = json.loads(response.text)
                print("Got information fo a user successful",response_data)
            else:
                response_data = json.loads(response.text)
                print("Get user request failed with status code:", response_data)

    @task
    def delete_user(self):
        flag=random.randint(0,1)
        global created_user
        if flag and len(created_user)>5:
            print("Deleting user")
            print('LENGHT OF CREATED_USER',len(created_user)) 
            user = user=created_user[random.randint(0, len(created_user)-1)]
            print("USER GOIG TO DELETE", user)
            response = self.client.delete("http://backend_service:8000/user", json={"user_id": user})
            if response.status_code == 204:
                print("User deleted successful user_id", user)
            else:
                print("DELETE user request failed with status code:", response.status_code)

    @task
    def update_user(self):
        print("uupdating information of a  user")
        global created_user
        global user_names_list
        if len(created_user)>=1:
            name=user_names_list[random.randint(0, 49)]
            client_id = created_client[random.randint(0, len(created_client)-1)]
            contact ="+91 " + "".join([str(random.randint(0, 9)) for _ in range(10)])
            user = user=created_user[random.randint(0, len(created_user)-1)]
            data={
                    "user_id":2,
                    "client_id":247,
                    "name":name,
                    "username":"new delhi",
                    "contact":contact,
                    "email":"vk@gmail.com",
                    "role_id":2
                } 
            response=self.client.patch("http://backend_service:8000/user", json=data)
            if response.status_code == 200:
                print("User updated successful")
            else:
                response_data = json.loads(response.text)
                print("update user request failed with status code:", response_data)

    @task
    def create_client(self):
        global created_client
        global user_names_list
        print("creating new client")
        name=user_names_list[random.randint(0, 49)]
        contact ="91" + "".join([str(random.randint(0, 9)) for _ in range(10)])
        data={
            "name":name,
            "address":"new delhi okhal phase 3",
            "contact":contact,
            "email":"anukul@gmail.com"
        } 
        response=self.client.put("http://backend_service:8000/client", json=data)
        if response.status_code == 201 or response.status_code == 200 :
            response_data = json.loads(response.text)
            created_client.append(response_data['client']['id'])
            print("Client created successful",response_data['client']['id'])
        else:
            print("PUT request failed with status code:", response.status_code)

    @task
    def create_consignment(self):
        global created_consignment
        global created_client
        global created_user
        user=created_user[0]
        if len(created_user)>=1:
            user = user=created_user[random.randint(0, len(created_user)-1)]
        if len(created_client):
            client=created_client[random.randint(0, len(created_client)-1)]
            print("creating new consignemnt")
            data={
                    "created_by_id":2,
                    "client_id":client,
                    "name":"con10",
                    "type":1
                }
            response=self.client.put("http://backend_service:8000/consignment", json=data)
            if response.status_code == 201 or response.status_code == 200:
                response_data = json.loads(response.text)
                created_consignment.append(response_data)
                print("Consignment created successful",response_data)
            else:
                response_data = json.loads(response.text)
                print("PUT request failed with status code:", response_data)

    @task
    def get_info_of_a_consignment(self):
        global created_consignment
        if len(created_consignment)>1:
            con_id=created_consignment[random.randint(0, len(created_consignment)-1)]
            data={
                    "con_id":1
                }
            response=self.client.get("http://backend_service:8000/consignment", json=data)

            if response.status_code == 201 or response.status_code == 200:
                response_data = json.loads(response.text)
                print("Got info of a consignemnt successful",response_data)
            else:
                response_data = json.loads(response.text)
                print("GET request failed with status code:",response_data)

    @task
    def get_all_consignment_of_client(self):
        global created_client
        if len(created_client):
            client=created_client[random.randint(0, len(created_client)-1)]
            print("creating new consignemnt")
            data={
                    "client_id":1
                }
            response=self.client.get("http://backend_service:8000/consignments", json=data)
            if response.status_code == 200:
                response_data=json.loads(response.text)
                print("Got all consignment of a client successful",response_data)
            else:
                print("GET request failed with status code:", response.status_code)


    @task
    def add_log_In_consignemnt(self):
        print("Adding new log in consignemnt")
        global created_consignment
        global created_log
        if len(created_consignment):
            cons_id=created_consignment[random.randint(0, len(created_consignment)-1)]
            data={
                    "con_id":1,
                    "barcode":"BARCODE13",
                    "length":2.3,
                    "volume":8.6
                }
            response=self.client.put("http://backend_service:8000/log", json=data)
            if response.status_code == 200 or response.status_code:
                response_data = json.loads(response.text)
                created_log.append(response_data.get('document_id'))
                print("Log added successful")
            else:
                print("PUT request failed with status code:", response.status_code)

    @task
    def get_info_of_a_log(self):
        global created_log
        if len(created_log):
            log_id=created_log[random.randint(0, len(created_log)-1)]
            data={
                    "id":1
                }
            response=self.client.get("http://backend_service:8000/log", json=data)
            if response.status_code == 200 or response.status_code == 201:
                print("Got info of a log  successful")
            else:
                print("GET request failed with status code:", response.status_code)
        
    @task
    def get_all_logs_of_consignment(self):
        global created_consignment
        if len(created_consignment):
            cons_id=created_consignment[random.randint(0, len(created_consignment)-1)]
            data={
                    "con_id":1
                }
            response=self.client.get("http://backend_service:8000/logs", json=data)
            if response.status_code == 200:
                print("Got All logs of a consignment")
            else:
                print("GET request failed with status code:", response.status_code)

    @task
    def get_users_of_client(self):
        global created_client
        if len(created_client):
            client=created_client[random.randint(0, len(created_client)-1)]
            data={
                    "client_id":1
                }
            response=self.client.get("http://backend_service:8000/users", json=data)
            if response.status_code == 200:
                print("Got all users of a client")
            else:
                print("PUT request failed with status code:", response.status_code)