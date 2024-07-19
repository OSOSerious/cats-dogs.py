import sqlite3
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('cats.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cats
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, chip_id TEXT, phone TEXT)''')
    conn.commit()
    conn.close()

init_db()

def generate_chip_id():
    return f"CHIP-{random.randint(1000000, 9999999)}"

def raise_kitten(kitten):
    stages = ["bottle_fed", "eating_solids", "potty_trained", "chipped"]
    for stage in stages:
        if stage not in kitten or not kitten[stage]:
            return {"error": f"Kitten needs to be {stage.replace('_', ' ')}"}
    
    # If all stages are complete, return a cat
    chip_id = generate_chip_id()
    cat = {
        "name": kitten["name"],
        "age": kitten["age"] + 1,
        "type": "cat",
        "chip_id": chip_id
    }
    
    # Store in database
    conn = sqlite3.connect('cats.db')
    c = conn.cursor()
    c.execute("INSERT INTO cats (name, age, chip_id, phone) VALUES (?, ?, ?, ?)",
              (cat["name"], cat["age"], cat["chip_id"], kitten["phone"]))
    conn.commit()
    conn.close()
    
    return cat

@app.route('/raise_kitten', methods=['POST'])
def handle_kitten():
    kitten = request.json
    cat = raise_kitten(kitten)
    return jsonify(cat)

@app.route('/check_chip/<chip_id>', methods=['GET'])
def check_chip(chip_id):
    conn = sqlite3.connect('cats.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cats WHERE chip_id = ?", (chip_id,))
    cat = c.fetchone()
    conn.close()
    
    if cat:
        return jsonify({"status": "Found", "name": cat[1], "age": cat[2], "phone": cat[4]})
    else:
        return jsonify({"status": "Not found"})

if __name__ == '__main__':
    app.run(debug=True)
