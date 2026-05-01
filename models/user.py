from peewee import *
from datetime import datetime
from .conn import BaseModel


#admin 
class AllowedEmail(BaseModel):
    email = CharField(unique=True)
    assigned_role = CharField()
    is_used = BooleanField(default=False)

#-----------

class User(BaseModel):
    user_id = AutoField()
    username = CharField(unique=True)
    hashed_password = CharField()
    firstName = CharField(max_length=15)
    lastName = CharField(max_length=15)
    email = CharField(unique=True)
    role = CharField(null=True) # admin, agent, customer,
    email_verified = BooleanField(default=False)
    is_active = BooleanField(default=False)
    last_login = DateTimeField(null=True)
    
class AccessToken(BaseModel):
    user = ForeignKeyField(User, backref="access_tokens")
    token_hash = CharField(unique=True, index=True)
    token_type = CharField() # portal_access, email_verification, password_reset
    expires_at = DateTimeField(null=True)
    used_at = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)
    

class AgentDetails(BaseModel):
    user = ForeignKeyField(User, backref="agent_details", unique=True)
    employee_number = CharField(200, unique=True)
    hire_date = DateTimeField()
    default_commission_rate = DecimalField()
    
    def save(self,*args, **kwargs):
        if self.user.role != "agent":
            raise ValueError("Invalid Role")
        return super().save(*args,**kwargs)
    
class CustomerDetails(BaseModel):
    user = ForeignKeyField(User, backref="customer_details", unique=True)
    customer_number = CharField(200, unique=True)
    preferred_contact_method = CharField() # email, sms, whatsapp 
    preferred_payment_method = CharField() # cash, installment, bank_transfer
    notes = TextField()
    
    def save(self, *args, **kwargs):
        if self.user.role != "customer":
            raise ValueError("Invalid Role")
        return super().save(*args, **kwargs)
    