import re
from flask_pymongo import ObjectId

def checkEmail(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}\.?[a-z]{1,2}$"
   if re.match(pat,s):
      return True
   return False

def checkAesKeyByteArray(s):
   pat = "^\[(((((0x[0-9a-fA-F]{2}),){15})(0x[0-9a-fA-F]{2}))|((((0x[0-9a-fA-F]{2}),){23})(0x[0-9a-fA-F]{2}))|((((0x[0-9a-fA-F]{2}),){31})(0x[0-9a-fA-F]{2})))\]$"
   if re.match(pat,s):
      return True
   return False

def checkAesIVByteArray(s):
   pat = "^\[((0x[0-9a-fA-F]{2}),){15}(0x[0-9a-fA-F]{2})\]$"
   if re.match(pat,s):
      return True
   return False

def str2bytes(datos):
   #Primero tengo que convertir los datos a lista
   temp = datos.strip('][')#.split(',')
   temp = temp.replace(",", " ")
   temp = temp.replace("0x", "")
   b = bytearray.fromhex(temp)
   #functools.partial(bytes,datos, "utf8")
   
   return b

def checkIpAddress(s):
   pat = "(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
   if re.match(pat,s):
      return True
   return False

def checkIpPortInt(port):
   if port > 0 and port <= 65535:
      return True
   return False

class User():
   def __init__(self, user_dict): #Paso la base de datos para poder hacer verificaciones contra lo actual y no lo almacenado
      self.id = str(user_dict['_id'])  #Paso el ID a texto para que Flask lo pueda guardar
      self.email = user_dict['email']  
      self.nombre = user_dict['fullname']
      self.is_authenticated = True #El objeto solo se crea si alguna vez se autenticó en el sistema
      self.is_anonymous = False #No trabajo con este tipo de usuarios
      self.is_active = user_dict['is_active']
      self.is_admin = user_dict['is_admin']

   def get_id(self):
      # Devuelve el ID del usuario como cadena
      return self.id