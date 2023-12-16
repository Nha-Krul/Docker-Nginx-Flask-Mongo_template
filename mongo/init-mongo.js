// CONFIGURACION DE LA DB
db.createUser({
    user: "root",
    pwd: "pAsswOrdSeGuRo.1",
    roles: [
        {
            role: "readWrite",
            db: "APP_Services",
        },
    ],
});

db = new Mongo().getDB("APP_Services");

// CONGIGURACION DE LOS USUARIOS 
try {
    db.createCollection("users", { capped: false });
} catch {
    console.log("Already exists")
}

db.users.insertMany([{
    "username": "admin", 
    "password": "pbkdf2:sha256:260000$bUwYtEBUIDwMt4fh$ab97b78244823a6426f9fbcd081bbd9329c4971d249263561b630e80f07a407d", //administrador
    "email" : "admin@admin.com",
    "fullname" : "Administrador",
    "is_active": true,
    "is_admin": true
}]);
