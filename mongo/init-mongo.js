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

db = new Mongo().getDB("ATSA_Services");

// CONGIGURACION DE LOS USUARIOS 
try {
    db.createCollection("users", { capped: false });
} catch {
    console.log("Already exists")
}

db.users.insertMany([{
    "username": "admin", 
    "password": "c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec", //admin
    "email" : "admin@admin.com",
    "fullname" : "Admin",
    "isActive": true,
    "isAdmin": true
}]);
