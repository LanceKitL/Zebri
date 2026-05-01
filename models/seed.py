from models.conn import db
from user import User, AccessToken, AgentDetails, CustomerDetails, AllowedEmail
from inventory import Supplier,Supply,Vehicle 

def run():
    db.connect()
    db.create_tables([User, AccessToken, AgentDetails, CustomerDetails, AllowedEmail, Supply, Supplier, Vehicle])      
    db.close()
    
run()