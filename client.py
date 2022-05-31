''' 
' Client.py
' Generates pairings and groupings for key generation
' Input json file name, length of key generation, qkd tpye ('Bell' or 'BB84'), output is filled in json file
' Nayana
'''
import sys
import random
import json

# for Bell State QKD
# A: 01, 23
# B: 02, 13
# C: 03, 12

# 00: phi+phi-
# 01: phi-phi+
# 10: psi+psi-
# 11: psi-psi+

#for BB84 QKD
# 0: Z
#1

# Values that correspond to pairings of 
pairings_list = [[[0, 1], [2, 3]], [[0, 2], [1, 3]], [[0, 3], [1, 2]]]

bell_state_grouping = [0, 1, 2, 3]

measurement_basis = ['X', 'Z']

def generate_BB84_guess(key_length):
    #decide whether to use X basis or right basis
    random.seed()
    bases = []
    init = []   #alice inits in either 0 or 1

    #for both alice and bob
    for _ in range(key_length):
        measurement_choice = measurement_basis[random.randrange(0, len(measurement_basis))]
        bases.append(measurement_choice)

    #alice also chooses between 0 and 1
    for _ in range(key_length):
        init_choice = random.randint(0, 1)
        init.append(init_choice)
    json_output = {
        "type": "BB84",
        "bases": bases,
        "init": init
    }

    return json_output



def generate_pairings_and_groupings_bell(key_length):
    #start random generation
    random.seed() #uses system time
    pairings = []
    groupings = []

    for _ in range(key_length):
        random_pair = pairings_list[random.randrange(0, len(pairings_list))]
        pairings.append(random_pair)
    
    for _ in range(key_length):
        random_grouping = bell_state_grouping[random.randrange(0, len(bell_state_grouping))]
        groupings.append(random_grouping)
    
    json_output = {
        "type": "Bell",
        "pairings": pairings,
        "groupings": groupings
    }

    return json_output

def generate_guesses(outfile, key_length, qkd_type):
    
    if qkd_type == "Bell":
        json_output = generate_pairings_and_groupings_bell(key_length)
    elif qkd_type == "BB84":
        json_output = generate_BB84_guess(key_length)
    else:
        print("QKD TYPE ERROR")
    
    # output to json file
    with open(outfile, "w") as fp:
        json.dump(json_output, fp)

if __name__ == "__main__":
    if  len(sys.argv) != 4:
        print("Usage: python3 client.py [outfile name] [key length] [qkd type 'Bell' or 'BB84']")
        exit(1)

    outfile = sys.argv[1]
    key_length = int(sys.argv[2])
    qkd_type = sys.argv[3]
    
    generate_guesses(outfile, key_length, qkd_type)

