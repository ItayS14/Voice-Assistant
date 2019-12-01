from flask import Flask
from Server import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    house_id = db.Column(db.Integer,db.ForeignKey('house.id'))
    profile_image = db.Column(db.String(32),nullable=False,default='default.jpg')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
 
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    device_type_id = db.Column(db.Integer) # Maybe need to convert this to db.ForeignKey
    options = db.Column(db.String(100)) 
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)
   
    def __repr__(self):
        return f"Device('{self.device_name}', Type: {self.device_type_id})"

#Need to think how to connect an house to the server
class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    devices = db.relationship('Device', backref='house', lazy=True)
    users = db.relationship('User', backref='house', lazy=True)
    
    def __repr__(self):
        return f"House('{self.name}', Devices: {self.devices}, Users: {self.users})"


class DeviceType(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"DeviceType({self.device_type_id})"

#Implementation of this model might vastly change
class Command(db.Model):
    index = db.Column(db.Integer,primary_key=True)
    command_words = db.Column (db.String(5000)) # All the words that can describe the command, as a list
    
    def __repr__(self):
        return f"Command('{self.index}': {self.command_words})"
