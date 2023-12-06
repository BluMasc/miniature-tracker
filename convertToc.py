import json

# Load the initial JSON from a file
with open('C:\\Users\\Gerrit Alpmann\\Desktop\\Projects\\miniature-tracker\\modelsTest.json', 'r') as file:
    data = json.load(file)

# Transform Minis into a list of dictionaries
minis_list = [{"id": int(key), **value} for key, value in data["Minis"].items()]

# Update the data with the modified Minis structure
data["Minis"] = minis_list

# Save the updated data to a file
with open('C:\\Users\\Gerrit Alpmann\\Desktop\\Projects\\miniature-tracker\\output.json', 'w') as file:
    json.dump(data, file, indent=4)