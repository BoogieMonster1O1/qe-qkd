"""
" Nayana Tiwari
" Quantum Key Distribution
" Runs full service of creating a quantum key of specified length
"""
from client import generate_guesses
from quantum_computer import run_quantum_circuits
from key_generation import generate_keys
import sys

def check_keys(alice, bob):
    if alice != bob:
        print("ERROR: KEYS ARE DIFFERENT")
        exit(1)

def qkd(alice_json, bob_json, qkd_type, key_length):
    correction_bits = 1
    attempt_key_length = key_length * 2

    #Generate Guesses for Alice and Bob
    generate_guesses(alice_json, attempt_key_length, qkd_type)
    generate_guesses(bob_json, attempt_key_length, qkd_type)

    #Run circuits
    run_quantum_circuits(alice_json, bob_json)

    #Generate the key
    generate_keys(alice_json, bob_json, correction_bits)

    check_keys(alice_json["key"], bob_json["key"])

def main():
    key_length = int(sys.argv[1])
    qkd_type = sys.argv[2]
    alice_json = "alice.json"
    bob_json = "bob.json"

    alice_final_key = ""
    bob_final_key = ""
    counter = 0

    while key_length > len(alice_final_key):
        qkd(alice_json, bob_json, qkd_type, key_length)

        alice_final_key += alice_json["key"]
        bob_final_key += bob_json["key"]
        counter += 1

    #truncate if needed
    alice_final_key = alice_final_key[:key_length - 1]
    bob_final_key = bob_final_key[:key_length - 1]

    check_keys(alice_final_key, bob_final_key)
    print("Generated key for qkd type {0} of length {1} in {2} runs of qkd".format(qkd_type, key_length, counter))

if __name__ == "__main__":
    main()
    



