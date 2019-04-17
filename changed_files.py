import os
import pickle
import hashlib
try:
    with open('db.pickle', 'rb') as f:
        ldb = pickle.load(f)
except IOError:
    ldb = []
db = dict(ldb)
fdump = open('db.files', 'w', newline="\n")
for root, dirs, files in os.walk("./"):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            file_path = file_path.replace('\\', '/')
            checksum = hashlib.md5(open(file_path, "rb").read()).hexdigest()
            if db.get(file_path, None) != checksum:
                print(file_path + " changed")
                fdump.write(file_path + '\n')
                db[file_path] = checksum
pickle.dump(db, open('db.pickle', 'wb'))
fdump.close()
