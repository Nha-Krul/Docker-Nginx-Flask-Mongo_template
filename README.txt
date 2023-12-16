DOCKER+NGINX+FLASK+MONGO_TEMPLATE

This python's project template was created as a base project for new applications.

It uses Docker, Mongo, Nginx and Flask to deploy the application in production environment.
Inside the "documentation" folder you can find all the information regarding this project structure




NGINX:

    Certificates:
        Generate private key:
        openssl genpkey -algorithm RSA -out server.key

        Generate cerificate request:
        openssl req -new -key server.key -out request.csr

        Sign the request with the private key:
        openssl x509 -req -days 365 -in request.csr -signkey server.key -out server.crt

        Eliminate the use of password from the key:
        openssl rsa -in server.key -out private_without_passphrase.key

    Configuration:
        Inside the folder "conf.d" you can edit the Nginx server Configuration.
        

FRONTEND:


BACKEND:

MONGO:
    Mongo use the official Docker image. For the correct installation of Mongo is very important to configure the environment variables inside the ".env" file.
    You can test the Mongo container with:
        sudo docker-compose build
        sudo docker-compose up mongodb

    If everything is ok, you can test the connection with MongoDBCompass or running "pruebaMongo.py". Remember to edit "pruebaMongo.py" with the correct USER, PASSWORD, and DATABASE

    