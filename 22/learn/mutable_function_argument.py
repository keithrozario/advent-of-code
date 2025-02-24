def test(value: int=0, temp_dict: dict={}):
    temp_dict["value"] = temp_dict.get("value", 0) + value
    return temp_dict

print(test(1))
print(test(1))
print(test(1))
print(test(1, {}))
print(test(1, {}))
print(test(1))

## output
# {'value': 1}
# {'value': 2}
# {'value': 3}
# {'value': 1}
# {'value': 1}
# {'value': 4}


"""

Actually, this is not a design flaw, and it is not because of internals or performance.
It comes simply from the fact that functions in Python are first-class objects, 
and not only a piece of code.

As soon as you think of it this way, then it completely makes sense: 
a function is an object being evaluated on its definition; 
default parameters are kind of "member data" and therefore their state may change from one call 
to the other - exactly as in any other object.

https://stackoverflow.com/questions/9158294/good-uses-for-mutable-function-argument-default-values
https://web.archive.org/web/20200221224620id_/http://effbot.org/zone/default-values.htm
"""
