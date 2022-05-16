'''
' Uses output of quantum computation to generate key using Alice and Bob's pairings and groupings
' Classical communication from architecture
' Alexander
'''
from re import A
import sys
import json
import random

class AttackerError(Exception):
    pass

def check_eavesdropper_bell(alice_json, bob_json, check_index):
    alice_initial_pairings = alice_json["pairings"]
    alice_initial_groupings = alice_json["groupings"]

    bob_initial_pairings = bob_json["pairings"]
    bob_initial_groupings = bob_json["groupings"]

    if (alice_initial_pairings[check_index] != bob_initial_pairings[check_index]
            or  alice_initial_groupings[check_index] != bob_initial_groupings[check_index]):
        raise AttackerError()

def check_eavesdropper_bb84(alice_json, bob_json, check_index):
    indices = alice_json["correct measurements"]
    alice_init_bases = alice_json["bases"]
    bob_init_bases = bob_json["bases"]

    if alice_init_bases[check_index] != bob_init_bases[check_index]:
        raise AttackerError()

qkd_eavesdropper_check = {"Bell": check_eavesdropper_bell, "BB84": check_eavesdropper_bb84}

def check_results_for_eavesdropper(alice_json, bob_json, correction_bits, qkd_type):
    indices = alice_json["correct_measurements"]

    random.seed()

    i = 0
    while i < correction_bits:
        # Check one bit for eavesdropper
        check_index = random.choice(indices)
        indices.remove(check_index)

        try:
            #check specific to the type of QKD used
            qkd_eavesdropper_check[qkd_type]
        except AttackerError:
            raise AttackerError
        
        i += 1

    alice_json["correct_measurements"] = indices
    bob_json["correct_measurments"] = indices

    return alice_json, bob_json
    
def generate_bell_key(json):
    bell_group_codes = ["00","01","10","11"]

    indices = json["correct_measurements"]
    init_groupings = json["groupings"]
    # generate key
    key = ""
    for i in indices:
        key += bell_group_codes[init_groupings[i]]
    return key

def generate_bb84_key(json):
    indices = json["correct measurements"]
    init_bases = json["bases"]
    #generate key
    key = ""
    for i in indices:
        if init_bases[i] == 'Z':
            key += '0'
        elif init_bases[i] == 'X':
            key += '1'
    #TODO: add two bits?

    return key


def generate_keys(alice_fname, bob_fname, correction_bits):
    #alice and bob's guesses have gone through a QC

    with open(alice_fname, "r") as f:
        alice_json = json.load(f)
    with open(bob_fname, "r") as f:
        bob_json = json.load(f)

    qkd_type = alice_json["type"]

    check_results_for_eavesdropper(alice_json, bob_json, correction_bits, qkd_type)
    
    if qkd_type == "Bell":
        #Use correct measurements to generate keys INDIVIDUALLY
        alice_json["key"] = generate_bell_key(alice_json)
        bob_json["key"] = generate_bell_key(bob_json)
    
    elif qkd_type ==  "BB84":
        #Use correct measurements to generate keys INDIVIDUALLY
        alice_json["key"] = generate_bb84_key(alice_json)
        bob_json["key"] = generate_bb84_key(bob_json)

    #Send codes to users
    with open(alice_fname, "w") as f:
        json.dump(alice_json, f)
    with open(bob_fname, "w"):
        json.dump(bob_json, f)


if __name__ == "__main__":
    if  len(sys.argv) != 4:
        print("Usage: python3 key_generation.py [alice fname] [bob fname] [# of correction bits]")
        exit(1)

    alice_fname = sys.argv[1]
    bob_fname = sys.argv[2]
    correction_bits = int(sys.argv[3]) #how many bits to check for attacker with

    generate_keys(alice_fname, bob_fname, correction_bits)






    

        


        
