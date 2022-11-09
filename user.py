import btree

class User:
    def __init__(self, name, password, imei, batt):
        self.name = name
    
    
    try:
        f = open("mydb_user", "r + b")
    except:
        f = open("mydb_user", "w + b")
        print("File")
        
        db = btree.open(f)
        self.data = {}

        for key in db:
            self.data[key] = db[key]

        db.flush()
        db.close()
        f.close()
        
        
        
        
        