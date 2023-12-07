import requests
import json

# URL a la que enviarás el JSON
url = "https://172.19.100.244/back_servicio_1"

# Datos que deseas enviar en formato JSON
datos_json = {
    "nombre": "Juan",
    "edad": 25,
    "ciudad": "Ejemplo City"
}

# Convierte el diccionario a una cadena JSON
datos_json_str = json.dumps(datos_json)

# Configura las cabeceras para indicar que estás enviando datos en formato JSON
headers = {'Content-type': 'application/json'}

# Desactiva la verificación SSL para certificados autofirmados
verify_ssl = False

# Envía la solicitud POST con los datos JSON a la URL
respuesta = requests.post(url, data=datos_json_str, headers=headers, verify=verify_ssl)

# Verifica el estado de la respuesta
if respuesta.status_code == 200:
    print("Solicitud exitosa. Respuesta:")
    print(respuesta.text)
else:
    print(f"Error en la solicitud. Código de estado: {respuesta.status_code}")
    print(respuesta.text)