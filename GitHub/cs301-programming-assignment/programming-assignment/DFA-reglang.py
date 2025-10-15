# Beckett O'Reilly, River Costello, Johnson Schwede
# CS301 Programming Assignment
# October 13, 2025

# Converting DFA to regular expression
# We *almost* correctly calculate the regular expression.
# Any alphabet can be used. We simplify and eliminate
# unnecessary parentheses.


epsilon = '\u03B5'
null = '\u2205'

# Regular expression helpers 
def union(a, b):
    if a in (null, ''): return b
    if b in (null, ''): return a
    if a == b: return a
    # Flatten nested unions and remove duplicates
    terms = []
    for part in [a, b]:
        if part.startswith('(') and part.endswith(')') and '+' in part:
            part = part[1:-1]
        for t in part.split('+'):
            if t not in terms:
                terms.append(t)
    return '+'.join(terms) if len(terms) == 1 else '(' + '+'.join(terms) + ')'

def concatenate(a, b):
    if null in (a, b): return null
    if a == epsilon: return b
    if b == epsilon: return a
    # Remove unnecessary parentheses if safe
    if a.startswith('(') and a.endswith(')') and '+' not in a:
        a = a[1:-1]
    if b.startswith('(') and b.endswith(')') and '+' not in b:
        b = b[1:-1]
    return a + b

def kleene_star(x):
    if x in (null, epsilon, ''): 
        return epsilon

    # Remove outer parentheses if they wrap a top-level union
    if x.startswith('(') and x.endswith(')') and '+' in x:
        inner = x[1:-1]
        terms = inner.split('+')
        # Remove ε from union
        terms = [t for t in terms if t != epsilon]
        if not terms:
            return epsilon
        elif len(terms) == 1:
            x = terms[0]
        else:
            x = '(' + '+'.join(terms) + ')'

    # Remove unnecessary parentheses for single symbols
    if x.startswith('(') and x.endswith(')') and '+' not in x:
        x = x[1:-1]

    return f"{x}*"

# Input DFA 
alphabet = input("Enter alphabet elements (e.g., 01 for {0,1}): ")
alphabet_list = [c for c in alphabet]

num_states = int(input("Enter number of states (0..n-1): "))
delta_list = []

for state in range(num_states):
    temp = input(f"Enter transitions for state {state} as comma-separated destination states for each alphabet symbol: ")
    temp_delta = [int(x) for x in temp.split(',')]
    delta_list.append(temp_delta)

accepting_states = input("Enter accepting states as comma-separated integers: ")
F = [int(x) for x in accepting_states.split(',')]

# Add temp start and temp final states 
temp_start = num_states
temp_final = num_states + 1

# Expand delta_list for temp states
delta_list.append([null]*len(alphabet_list))  # temp start
delta_list.append([null]*len(alphabet_list))  # temp final

# Update number of states
num_states += 2
all_states = list(range(num_states))

# Initialize Regular expression matrix R[u][v] 
R = [[null for _ in range(num_states)] for _ in range(num_states)]

# Fill R with original transitions
for u in range(len(delta_list)-2):  # original states
    for i, v in enumerate(delta_list[u]):
        symbol = alphabet_list[i]
        if R[u][v] == null:
            R[u][v] = symbol
        else:
            R[u][v] = union(R[u][v], symbol)
    R[u][u] = union(R[u][u], epsilon)  # self-loop

# temp start points to real start (state 0) via epsilon
R[temp_start][0] = epsilon

# All accepting states point to temp final via epsilon
for f in F:
    R[f][temp_final] = epsilon

# State elimination 
# Eliminate all states except temp start and temp final
for q in all_states:
    if q in (temp_start, temp_final):
        continue
    for i in all_states:
        if i == q:
            continue
        for j in all_states:
            if j == q:
                continue
            R[i][j] = union(R[i][j], concatenate(concatenate(R[i][q], kleene_star(R[q][q])), R[q][j]))
    # Remove outgoing/incoming transitions of eliminated state
    for k in all_states:
        R[k][q] = null
        R[q][k] = null

# Final Regular expression 
reg_exp = R[temp_start][temp_final]

print("\nFinal Regular Expression:")
print(reg_exp)
