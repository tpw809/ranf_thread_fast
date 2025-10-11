"""https://stackoverflow.com/questions/50156550/test-if-dictionary-key-exists-is-not-none-and-isnt-blank

Want to allow user to either omit the key in the dictionary or set the key to None.
"""

mydict = {
    "a":"alpha",
    "b":0,
    "c":False,
    "d":None,
    "e":"",
    "g":"   ",
}

#a,b,c should succeed, d,e,f,g should fail...
for k in "abcdefg":
    print(f"\nkey = {k}")
    v = mydict.get(k)
    print(f"v = {v}")
    print(v==None)
    if v and v.strip():
        print(k,"I am here and have stuff")
    else:
        print(k,"I am incomplete and sad")

# if v is not None and (not isinstance(v,str) or v.strip()):

# use case:
print("\nMy Use Case:\n")
# omitted key:
v = mydict.get('f')
print(f"v = {v}")
print(v==None)

# value is set to None:
v = mydict.get('d')
print(f"v = {v}")
print(v==None)
