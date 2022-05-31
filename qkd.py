"""
" Nayana Tiwari
" Quantum Key Distribution
" Runs full service of creating a quantum key of specified length
"""
from client import generate_guesses
from quantum_computer import run_quantum_circuits
from key_generation import generate_keys
import sys
import json

def save_for_later(test_fname, alice_json, bob_json):
    with open(test_fname, "a+") as f_test:
        json.dump(alice_json, f_test)
        f_test.write("\n")
        json.dump(bob_json, f_test)
        f_test.write("\n")
    
    f_test.close()

def check_keys(alice_fname, bob_fname, test_fname): 
    with open(alice_fname, "r") as f_alice:
        alice_json = json.load(f_alice)
    with open(bob_fname, "r") as f_bob:
        bob_json = json.load(f_bob)
    save_for_later(test_fname, alice_json, bob_json)
    
    alice_key = alice_json["key"]
    bob_key = bob_json["key"]

    f_alice.close()
    f_bob.close()

    if alice_key != bob_key:
        print("ERROR: KEYS ARE DIFFERENT")
        exit(1)
    return alice_key, bob_key

def qkd(alice_json_fname, bob_json_fname, test_fname, qkd_type, key_length):
    correction_bits = 1
    attempt_key_length = key_length * 2

    #Generate Guesses for Alice and Bob
    generate_guesses(alice_json_fname, attempt_key_length, qkd_type)
    generate_guesses(bob_json_fname, attempt_key_length, qkd_type)

    #Run circuits
    run_quantum_circuits(alice_json_fname, bob_json_fname)

    #Generate the key
    generate_keys(alice_json_fname, bob_json_fname, correction_bits)

    return check_keys(alice_json_fname, bob_json_fname, test_fname)

def main():
    key_length = int(sys.argv[1])
    qkd_type = sys.argv[2]
    alice_json_fname = "alice_" + sys.argv[2] + "_" + sys.argv[3] + ".json"
    bob_json_fname = "bob_" + sys.argv[2] + "_" + sys.argv[3] + ".json"
    test_fname = sys.argv[2] + "_" + sys.argv[3] + ".json"
    outfile = "results.csv"

    alice_final_key = ""
    bob_final_key = ""
    counter = 0

    print("Attempting running alice and bob circuits for {0} {1}".format(qkd_type, sys.argv[3]))
    while key_length > len(alice_final_key):
         print("key is of length {0}".format(len(alice_final_key)))
         alice_key, bob_key = qkd(alice_json_fname, bob_json_fname, test_fname, qkd_type, key_length)

         alice_final_key += alice_key
         bob_final_key += bob_key
         counter += 1

    #truncate if needed, slicing is exclusive endpoints
    alice_final_key = alice_final_key[:key_length]
    bob_final_key = bob_final_key[:key_length]

    if alice_final_key != bob_final_key:
        print("ERROR: Final keys do not match")
        exit(1)

    fp = open(outfile, "a")
    print("Generated key for qkd type {0} of length {1} in {2} runs of qkd".format(qkd_type, key_length, counter))
    outline = "{0},{1},{2},{3}, {4}\n".format(key_length, qkd_type, counter, alice_final_key, alice_json_fname)
    fp.write(outline)
    fp.close()

if __name__ == "__main__":
    main()
    



