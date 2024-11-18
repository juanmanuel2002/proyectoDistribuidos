db = db.getSiblingDB('proyecto');

if(!db.getCollectionNames().includes('citas')){
    db.createCollection('citas');

    db.citas.insertOne({
            "nombre":"Pepito123",
            "fecha":"24/06/2002",
            "hora": "12 pm",
            "descripcion": "prueba"
    });

    db.citas.insertOne({
        "nombre":"Pepito123456",
        "fecha":"24/06/2002",
        "hora": "6 pm",
        "descripcion": "prueba2"
    });
    
}

if(!db.getCollectionNames().includes('usuarios')){
    db.createCollection('usuarios');

    db.usuarios.insertOne({
        "usuario": "admin",
        "password": "scrypt:32768:8:1$mKvwBydkSknMheHv$97c8a899e32910d9884e39f393fd2df74b41ac5679d87768133ce229645cc5e41c0d8b7244579e3d6a91741143762cb2443555b27bc0fd49c9f273fe9e3a7083"
    });
}
