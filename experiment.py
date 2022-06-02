"""
" Nayana Tiwari
" Run QKD for Bell and BB84 for many runs
" Understand randomness of each QKD
"""
import time, json
from client import generate_guesses
from quantum_computer import run_quantum_circuits

def experiment(alice_json_fname, bob_json_fname, qkd_type, seed1, seed2):
    attempt_key_length = 1000

    #Generate Guesses for Alice and Bob
    generate_guesses(alice_json_fname, attempt_key_length, qkd_type, seed1)
    generate_guesses(bob_json_fname, attempt_key_length, qkd_type, seed2)

    #Run circuits
    run_quantum_circuits(alice_json_fname, bob_json_fname)
    with open(alice_json_fname, "r") as f_alice:
        alice_json = json.load(f_alice)
    with open(bob_json_fname, "r") as f_bob:
        bob_json = json.load(f_bob)
    
    num_correct_measurements_bob = len(bob_json["correct_measurements"])
    num_correct_measurements_alice = len(alice_json["correct_measurements"])

    string = "QKD:{0} ATTEMPTS {1} CORRECT {2} {3}\n".format(qkd_type, attempt_key_length, num_correct_measurements_bob, num_correct_measurements_alice)
    return string

def main():
    seed1 = time.time()

    alice_fname_Bell = "alice_Bell.json"
    bob_fname_Bell = "bob_Bell.json"

    alice_fname_BB84 = "alice_BB84.json"
    bob_fname_BB84 = "bob_BB84.json"

    output_fname = "results.txt"
    output_fp = open(output_fname, "w+")

    seed2 = time.time()

    output_str = experiment(alice_fname_Bell, bob_fname_Bell, "Bell", seed1, seed2)
    output_fp.write(output_str)
    print(output_str)

    output_str = experiment(alice_fname_BB84, bob_fname_BB84, "BB84", seed1, seed2)
    output_fp.write(output_str)
    print(output_str)

    output_fp.close()


if __name__ == "__main__":
    main()