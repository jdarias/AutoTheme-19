# this reads a dictionary from a file
opts={}

with open("test.conf") as f:
    for line in f:
        (key, val)=line.split()
        opts[key]=val

print(opts)
print(type(opts["work_night"]))

# How to read a dictionary from a file in Python
# https://kite.com/python/answers/how-to-read-a-dictionary-from-a-file-in--python 

# Save a dictionary to a file
# https://pythonspot.com/save-a-dictionary-to-a-file/

# How to Check if a File or Directory Exists in Python
# https://linuxize.com/post/python-check-if-file-exists/ 
