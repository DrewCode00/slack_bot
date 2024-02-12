import json

with open("example.json", "r") as f:
    data = json.load(f)

print(data["Name"]) # Foo
print(data["Hobby"][1]) # video game
print(data["Grade"]["1st Semester"]["Calculus"]) # A

data["Location"] = "Boston"

with open("example.json", 'w') as f:
    json.dump(data, f)