db = db.getSiblingDB('proyecto');

if(!db.getCollectionNames().includes('citas')){
    db.createCollection('citas');
}

if(!db.getCollectionNames().includes('usuarios')){
    db.createCollection('usuarios');
}