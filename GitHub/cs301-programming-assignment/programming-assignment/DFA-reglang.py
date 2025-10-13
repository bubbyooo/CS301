# Beckett O'Reilly, River Costello, Johnson Schwede
# CS301 Programming Assignment
# October 13, 2025



alphabet = input("Enter alphabet elements. Exclude all brackets, commas, and spaces. ")
alphabet_list = []
for element in alphabet:
    alphabet_list.append(element)

more_states = 'y'
state = 0
delta_list = []
while(more_states == 'y'):
    temp_delta = input(f"Enter transition function for state {state}. Exclude all brackets, commas, and spaces. ")
    state += 1
    temp_delta_list = []
    for element in temp_delta:
        temp_delta_list.append(element)
    delta_list.append(temp_delta_list)
    more_states = input("Enter another state? (y/n) ")


accepting_states = input("Enter accepting states. Exclude all brackets, commas, and spaces. ")
F = []
for element in accepting_states:
    F.append(element)

print(f"Alphabet: {alphabet_list}, Delta: {delta_list}, F: {F}")


DFA = [alphabet, delta, F]

