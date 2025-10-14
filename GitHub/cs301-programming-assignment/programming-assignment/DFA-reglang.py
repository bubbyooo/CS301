# Beckett O'Reilly, River Costello, Johnson Schwede
# CS301 Programming Assignment
# October 13, 2025


epsilon = '\u03B5'
null = '\u2205'

# Generate alphabet
alphabet = input("Enter alphabet elements. Exclude all brackets, commas, and spaces. ")
alphabet_list = []
for element in alphabet:
    alphabet_list.append(element)

# Generates transition functions and list of lists to pass in as A
more_states = 'y'
state = 0
state_index = [[]]      # List of lists to pass in as A
delta_list = []
while(more_states == 'y'):
    temp_delta = input(f"Enter transition function for state {state}. Exclude all brackets, commas, and spaces. ")
    state_index.append(list(range(0,state+1)))
    state += 1
    temp_delta_list = []
    for element in temp_delta:
        temp_delta_list.append(int(element))
    delta_list.append(temp_delta_list)
    more_states = input("Enter another state? (y/n) ")


accepting_states = input("Enter accepting states. Exclude all brackets, commas, and spaces. ")
F = []
for element in accepting_states:
    F.append(int(element))

print(f"Alphabet: {alphabet_list}, Delta: {delta_list}, F: {F}")


DFA = [alphabet_list, delta_list, F]

def alpha_construction_step(A, u, v):
    print(f"path from {u} to {v} through {A}")
    # Base cases
    if len(A) == 0:
        # Base case 1
        if u == v:
            self_string = ""
            for element in delta_list[u]:
                if element == v:
                    if self_string == "":
                        self_string += alphabet_list[delta_list[u].index(element)]
                    else:
                        self_string += f" + {alphabet_list[delta_list[u].index(element)]}"
            if self_string == "":
                print(f"BC1 empty -- self_string: {self_string}")
                return epsilon
            else:
                print(f"BC1 ne -- self_string: {self_string}")
                return f"({self_string} + {epsilon})"
        # Base case 2 + 3
        else:
            self_string = ""
            for element in delta_list[u]:
                if element == v:
                    if self_string == "":
                        self_string += alphabet_list[delta_list[u].index(element)]
                    else:
                        self_string += f" + {alphabet_list[delta_list[u].index(element)]}"
            # Base case 3
            if self_string == "":
                print(f"BC3 -- self_string: {self_string}")
                return null
            # Base case 2
            else:
                print(f"BC2 -- self_string: {self_string}")
                return f"({self_string})"
            
    # Recursive case
    q = A[-1]
    state_step = state_index[len(A)-1]
    return alpha_construction_step(state_step, u, v) + " + " + alpha_construction_step(state_step, u, q) + \
        "(" + alpha_construction_step(state_step, q, q) + ")*" + alpha_construction_step(state_step, q, v)


regular_expression = ""
for state in F:
    regular_expression += alpha_construction_step(state_index[-1], 0, state)
print(regular_expression)
