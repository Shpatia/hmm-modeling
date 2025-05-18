import json

def save_1d_params(filename, a, d, n):
    data = {"a": a, "d": d, "n": n}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_1d_params(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["a"], data["d"], data["n"]
