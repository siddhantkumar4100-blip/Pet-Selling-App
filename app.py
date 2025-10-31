from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# -------------------------------
# Simulated Database
# -------------------------------
pets = [
    {"id": 1, "name": "Buddy", "breed": "Labrador", "price": 15000, "location": "Delhi", "language": "English"},
    {"id": 2, "name": "Simba", "breed": "Persian Cat", "price": 10000, "location": "Mumbai", "language": "Hindi"},
    {"id": 3, "name": "Max", "breed": "German Shepherd", "price": 20000, "location": "Chennai", "language": "English"},
]

# -------------------------------
# Fake Aadhar & PAN Verification
# -------------------------------
def verify_aadhar(aadhar_number):
    """Simulates Aadhar verification"""
    if len(aadhar_number) == 12 and aadhar_number.isdigit():
        return {"status": "verified", "aadhar": aadhar_number}
    return {"status": "invalid", "reason": "Aadhar number must be 12 digits"}

def verify_pan(pan_number):
    """Simulates PAN verification"""
    if len(pan_number) == 10 and pan_number[:5].isalpha() and pan_number[5:9].isdigit() and pan_number[-1].isalpha():
        return {"status": "verified", "pan": pan_number.upper()}
    return {"status": "invalid", "reason": "Invalid PAN format"}

# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def home():
    return render_template('index.html', pets=pets)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    aadhar = data.get("aadhar")
    pan = data.get("pan")

    aadhar_result = verify_aadhar(aadhar)
    pan_result = verify_pan(pan)

    if aadhar_result["status"] == "verified" and pan_result["status"] == "verified":
        return jsonify({"message": "Verification successful!"})
    else:
        return jsonify({"message": "Verification failed!", "details": {"aadhar": aadhar_result, "pan": pan_result}})

@app.route('/filter', methods=['GET'])
def filter_pets():
    breed = request.args.get('breed')
    price = request.args.get('price')
    location = request.args.get('location')
    language = request.args.get('language')

    filtered = pets
    if breed:
        filtered = [p for p in filtered if breed.lower() in p["breed"].lower()]
    if price:
        filtered = [p for p in filtered if p["price"] <= int(price)]
    if location:
        filtered = [p for p in filtered if location.lower() in p["location"].lower()]
    if language:
        filtered = [p for p in filtered if language.lower() in p["language"].lower()]

    return jsonify(filtered)

@app.route('/add_pet', methods=['POST'])
def add_pet():
    data = request.json
    new_pet = {
        "id": random.randint(100, 999),
        "name": data.get("name"),
        "breed": data.get("breed"),
        "price": int(data.get("price")),
        "location": data.get("location"),
        "language": data.get("language")
    }
    pets.append(new_pet)
    return jsonify({"message": "Pet added successfully!", "pet": new_pet})

if __name__ == '__main__':
    app.run(debug=True)
