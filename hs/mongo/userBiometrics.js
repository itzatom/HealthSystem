var mydb = db.getSiblingDB("healthsystem");
mydb.createUser({ user: "paziente", pwd : "passwdpaziente", roles : ["readWrite"]});
mydb.createUser({ user: "medico", pwd : "passwdmedico", roles : ["read"]}); 
