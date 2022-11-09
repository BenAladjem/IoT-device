import btree

class User:
    def __init__(self, name, password, imei, batt, db)
    
    
    try:
        f = open("mydb", "r + b")
    except:
        f = open("mydb", "w + b")
        print("File")
        
        db = btree.open(f)
        self.data = {}

        for key in db:
            self.data[key] = db[key]

        db.flush()
        db.close()
        f.close()