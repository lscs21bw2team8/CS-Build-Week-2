import hashlib
import requests

#Add your token here
token = "Token "
r = requests.get(url="https://lambda-treasure-hunt.herokuapp.com/api/bc" + "/last_proof", headers={"Authorization": token}).json()
proof = 0
last_proof = r.get("proof")
diff = r.get("difficulty")
print(f"last proof: {last_proof}")
print(f"difficulty: {diff}")
guess = f'{last_proof}{proof}'.encode()
guess_hash = hashlib.sha256(guess).hexdigest()
hash_start = ""
for i in range(diff):
    hash_start += "0"
print(f"leading zeros to find: {hash_start}")
while guess_hash[:diff] != hash_start:
    proof += 2
    new_proof = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(new_proof).hexdigest()
    #print(guess_hash)

r = requests.post(url="https://lambda-treasure-hunt.herokuapp.com/api/bc" + "/mine", json={"proof": proof}, headers={"Authorization": token})
print(f"good proof:  {proof}")
print(f"response: {r.json()}")
last_proof = proof
proof = 0