import csv

from bson.objectid import ObjectId
from typing import List
from pymongo import MongoClient


class DatabaseHandler:
    def __init__(self, db_name: str, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]


    def insert_social_network(self, name: str) -> ObjectId:
        social_networks = self.db.social_networks
        result = social_networks.insert_one({
            "name": name,
        })
        return result.inserted_id


    def insert_user(self, social_network_id: ObjectId, user_id: int, last_message: str, username='') -> ObjectId:
        users = self.db.users
        result = users.insert_one({
            "social_network_id": social_network_id,
            "user_id": user_id,
            "username": username,
            "last_message": last_message
        })
        return result.inserted_id


    def insert_qna(self, csv_filename: str) -> List[ObjectId]:
        qna = self.db.qna
        qna.drop()
        qna_data = []
        with open(csv_filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            for row in reader:
                question, answer = row
                qna_data.append({"question": question, "answer": answer})
        result = qna.insert_many(qna_data)
        return result.inserted_ids


    def insert_request(self, user_id: ObjectId, user_sn: ObjectId, user_chat_id: int, user_question: str) -> ObjectId:
        requests = self.db.requests
        result = requests.insert_one({
            "user_id": user_id,
            "sn_id": user_sn,
            "user_chat_id": user_chat_id,
            "user_question": user_question,
            "status": "waiting",
            "user_answer": "",
            "operator": ""
        })
        return result.inserted_id


    def insert_operator(self, username: str, password: bytes) -> ObjectId:
        operators = self.db.operators
        result = operators.insert_one({
            "username": username,
            "password": password
        })
        return result.inserted_id
    

    def get_operator(self, username: str) -> dict:
        operators = self.db.operators
        return operators.find_one({
            "username": username
        })
    
    
    def get_operator_by_id(self, op_id: ObjectId) -> dict:
        operators = self.db.operators
        return operators.find_one({
            "_id": op_id
        })


    def find_user(self, social_network_id: ObjectId, user_id: int) -> dict:
        users = self.db.users
        return users.find_one({
            "social_network_id": social_network_id,
            "user_id": user_id
        })
    

    def social_network_exists(self, social_network_name: str) -> ObjectId | None:
        users = self.db.social_networks
        sn = users.find_one({
            "name": social_network_name,
        })
        if sn:
            return sn['_id']
        return None
    

    def get_social_network_name(self, sn_id: ObjectId) -> str:
        social_networks = self.db.social_networks
        sn = social_networks.find_one(
            {"_id": sn_id}
        )
        return sn['name']


    def update_user_last_message(self, user_id: ObjectId, last_message: str):
        users = self.db.users
        result = users.update_one(
            {"_id": user_id},
            {"$set": {"last_message": last_message}}
        )
        return result.modified_count


    def get_all_questions(self) -> List[dict]:
        qna = self.db.qna
        return list(qna.find({}))


    def find_qna(self, question: str) -> dict:
        qna = self.db.qna
        return qna.find_one({
            "$or": [
                {"question": question}
            ]
        })


    def get_all_requests(self) -> List[dict]:
        requests = self.db.requests
        return list(requests.find({}))


    def update_request_status(self, request_id: ObjectId, status: str, answer: str, operator_username: str):
        requests = self.db.requests
        result = requests.update_one(
            {"_id": request_id},
            {"$set": {
                "status": status,
                "user_answer": answer,
                "operator": operator_username
            }}
        )
        return result.modified_count


    def close(self):
        self.client.close()