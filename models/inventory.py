from peewee import *
from datetime import datetime
from models.conn import BaseModel

class Supplier(BaseModel):
    supplier_id = AutoField()
    company_name = CharField(150)
    contact_name = CharField(100)
    contact_email = CharField(100)
    contact_phone = CharField(20)
    address = CharField(255)
    is_active = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)

class Supply(BaseModel):
    supply_id = AutoField()
    supplier = ForeignKeyField(Supplier, backref="supplies")
    part_name = CharField(150)
    part_number = CharField(50, unique=True)
    unit_cost = DecimalField()
    stock_qty = IntegerField(null=True)
    reorder_level = IntegerField(null=True)
    updated_at = DateTimeField(null=True)
    
class Vehicle(BaseModel):
    vehicle_id = AutoField()
    supplier = ForeignKeyField(Supplier, backref="vehicles")
    vin = CharField(17, unique=True)
    brand = CharField(50)
    model = CharField(50)
    year = IntegerField()
    color = CharField(50)
    seating_capacity = IntegerField()
    
    
