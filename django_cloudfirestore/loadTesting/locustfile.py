from locust import HttpUser, task,between
import json
import random

created_user=['008UcRv2DANQOXRUFCuW']
created_client=['3ccYKrB8V1DGK3uZ9lqo']
created_consignment=['05GK7lueHUpMrnQatDoS']
created_log=['024VTTtBQbvCLPQhjnsK']
user_names_list = ["Frank", "Grace", "Hannah", "Isaac", "Jack", "Kelly", "Liam", "Mia", "Nathan", "Olivia",
                    "Paul", "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xander", "Yara",
                    "Zoe", "Adam", "Ben", "Chloe", "Daisy", "Ethan", "Fiona", "George", "Holly", "Ian", "Jenny",
                    "Kevin", "Lucy", "Mike", "Nancy", "Oscar", "Penny", "Quincy", "Ruth", "Simon", "Tanya",
                    "Ulysses", "Violet", "William", "Xavier", "Yvonne", "Zack","vikesh","dheeraj","rahul","gopla"]
"""
    Python class for performance testing.
"""
class HelloWorldUser(HttpUser):

    wait_time = between(1, 2)

    @task
    def create_user(self):
        global created_user
        global created_client
        global user_names_list
        client_id = created_client[random.randint(0, len(created_client)-1)]
        name=user_names_list[random.randint(0, 49)]
        response=self.client.put("http://172.18.0.4:8001/user/", json={"client_id":client_id,"name":name,"username":name+"_user","contact":713654795,"role":["web","mobile"],"doc_type":"user"})
        if response.status_code == 200:                         
            response_data = json.loads(response.text)
            created_user.append(response_data.get('document_id'))
            print("user",created_user)
        else:
            # response_data = json.loads(response.text)
            print("PUT request failed with status code:",response.status_code)

    @task
    def get_user(self):
        global created_user
        if len(created_user)>=1:
            user=created_user[random.randint(0, len(created_user)-1)]
            response=self.client.get("http://172.25.0.2:8001/user/", json={ "id":user})
            if response.status_code == 200:
                response_data = json.loads(response.text)
                print("Got information fo a user successful",response_data.get('user'))
            else:
                print("Get request failed with status code:", response.status_code)

    @task
    def delete_user(self):
        flag=random.randint(0,1)
        global created_user
        if flag and len(created_user)>1:
            user = user=created_user[random.randint(0, len(created_user)-1)]
            response = self.client.delete("http://172.25.0.2:8001/user/", json={"id": user})
            if response.status_code == 204:
                print("User deleted successful user_id", user)
            else:
                print("DELETE request failed with status code:", response.status_code)

    @task
    def update_user(self):
        print("uupdating information of a  user")
        global created_user
        global user_names_list
        if len(created_user)>0:
            name=user_names_list[random.randint(0, 49)]
            user = user=created_user[random.randint(0, len(created_user)-1)]
            data={
                    "id":user,
                    "name":name,
                    "username":"new delhi",
                    "contact":541257796,
                    "email":"vk@gmail.com",
                    "doc_type":"user",
                    "role":["web","mobile"]
                } 
            response=self.client.patch("http://172.25.0.2:8001/user/", json=data)
            if response.status_code == 200:
                print("User updated successful")
            else:
                print("PUT request failed with status code:", response.status_code)

    @task
    def create_client(self):
        global created_client
        global user_names_list
        print("creating new client")
        name=user_names_list[random.randint(0, 49)]
        data={
            "doc_type":"client",
            "name":name,
            "address":"new delhi okhal phase 3",
            "contact":812547896,
            "email":"anukul@gmail.com"
        } 
        response=self.client.put("http://172.25.0.2/client/", json=data)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            created_client.append(response_data.get('document_id'))
            print("Client created successful")
        else:
            print("PUT request failed with status code:", response.status_code)

    @task
    def create_consignment(self):
        global created_consignment
        global created_client
        global created_user
        if len(created_client):
            client=created_client[random.randint(0, len(created_client)-1)]
            print("creating new consignemnt")
            data={
                    "client_id":client,
                    "created_by":"2tZlZDnZ0em0KxZl9pPL",
                    "name":"con10",
                    "type":1
                }
            response=self.client.put("http://172.25.0.2:8001/consignment/", json=data)
            if response.status_code == 200:
                response_data = json.loads(response.text)
                created_consignment.append(response_data.get('document_id'))
                print("Consignment created successful")
            else:
                print("PUT request failed with status code:", response.status_code)

    @task
    def get_info_of_a_consignment(self):
        global created_consignment
        if len(created_consignment):
            con_id=created_consignment[random.randint(0, len(created_consignment)-1)]
            data={
                    "con_id":con_id
                }
            response=self.client.get("http://172.25.0.2:8001/consignment/", json=data)
            if response.status_code == 200:
                response_data = json.loads(response.text)
                print("Got info of a consignemnt successful",response_data)
            else:
                print("GET request failed with status code:", response.status_code)

    @task
    def get_all_consignment_of_client(self):
        global created_client
        if len(created_client):
            client=created_client[random.randint(0, len(created_client)-1)]
            print("creating new consignemnt")
            data={
                    "client_id":client
                }
            response=self.client.get("http://172.25.0.2:8001/consignments/", json=data)
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
                    "con_id":cons_id,
                    "barcode":"BARCODE13",
                    "length":2.3,
                    "volume":8.6
                }
            response=self.client.put("http://172.25.0.2:8001/log/", json=data)
            if response.status_code == 200:
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
                    "id":log_id
                }
            response=self.client.get("http://172.25.0.2:8001/log/", json=data)
            if response.status_code == 200:
                print("Got info of a log  successful")
            else:
                print("GET request failed with status code:", response.status_code)
        
    @task
    def get_all_logs_of_consignment(self):
        global created_consignment
        if len(created_consignment):
            cons_id=created_consignment[random.randint(0, len(created_consignment)-1)]
            data={
                    "con_id":cons_id
                }
            response=self.client.get("http://172.25.0.2:8001/logs/", json=data)
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
                    "client_id":client
                }
            response=self.client.get("http://172.25.0.2:8001/users/", json=data)
            if response.status_code == 200:
                print("Got all users of a client")
            else:
                print("PUT request failed with status code:", response.status_code)

   