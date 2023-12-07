# Configura la conexión
#client = MongoClient('mongodb://root:pAsswOrdSeGuRo.1@172.19.100.244:27017/')

from pymongo import MongoClient

def test_connection():
    # Configura la conexión
    client = MongoClient('mongodb://root:pAsswOrdSeGuRo.1@172.19.100.244:27017/')

    # Prueba la conexión
    try:
        client.admin.command('ping')
        print("Conexión exitosa.")
        
        # Cambia la base de datos
        db_name = 'APP_Services'
        db = client[db_name]
        print(f"Cambiando a la base de datos: {db_name}")

        # Realiza operaciones en la nueva base de datos si es necesario
        # Ejemplo: consulta todos los documentos en una colección
        collection_name = 'servicio_1'
        documents = db[collection_name].find()

        print(f"Documentos en la colección {collection_name}:")
        for doc in documents:
            print(doc)

    except Exception as e:
        print(f"Error al conectar: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_connection()