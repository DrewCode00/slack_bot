import Json

with open("example.json", "r") as f:
    data = json.load(f)


    print(data["Name"])_# Foo
    print(data["Hobby"])
    _  # Video Game
    print(data["Grade"]["1st Semester"]["Calculate"])_# A

  data["Location"] = "Boston"

with open("example.json", 'W') as f:
    json.dump(data, f)