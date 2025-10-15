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
while more_states == 'y':
    temp_delta = input(
        f"Enter transition function for state {state}. Use space-separated integers. "
    ).strip().split()
    state_index.append(list(range(0, state + 1)))
    state += 1
    temp_delta_list = [int(x) for x in temp_delta]  # <-- keep only this
    delta_list.append(temp_delta_list)
    more_states = input("Enter another state? (y/n) ")


accepting_states = input("Enter accepting states (space-separated integers). ").strip().split()
F = [int(x) for x in accepting_states]

print(f"Alphabet: {alphabet_list}, Delta: {delta_list}, F: {F}")


DFA = [alphabet_list, delta_list, F]


def simplify(a1, a2, a3, a4):
    EPS, NULL = epsilon, null
    s = lambda x: (x or "").strip()
    is_eps = lambda x: s(x) == EPS
    is_null = lambda x: s(x) == NULL

    def strip_parens(x):
        x = s(x)
        if len(x) >= 2 and x[0] == '(' and x[-1] == ')':
            d = 0
            for i, ch in enumerate(x):
                if ch == '(': d += 1
                elif ch == ')': d -= 1
                if d == 0 and i != len(x) - 1: return x
            return x[1:-1]
        return x

    def has_top_plus(x):
        x = s(x); d = 0
        for ch in x:
            if ch == '(': d += 1
            elif ch == ')': d -= 1
            elif ch == '+' and d == 0: return True
        return False

    def par_if_union(x):
        x = s(x)
        return f"({x})" if x and (has_top_plus(x) or is_null(x)) else x

    def plus(x, y):
        x, y = s(x), s(y)
        if is_null(x): return y
        if is_null(y): return x
        if x == y:     return x
        return f"{x} + {y}"

    def cat(x, y):
        x, y = s(x), s(y)
        if is_null(x) or is_null(y): return NULL
        if is_eps(x): return y
        if is_eps(y): return x
        return par_if_union(x) + par_if_union(y)

    def star(x):
        x = strip_parens(x)
        if is_null(x) or is_eps(x): return EPS
        return (x if (len(x) == 1 or x.startswith('(')) else f"({x})") + "*"

    term2 = cat(cat(strip_parens(a2), star(a3)), strip_parens(a4))
    return strip_parens(plus(strip_parens(a1), term2))

def alpha_construction_step(A, u, v): # EDIT
    """
    α_A(u,v): regular expression for all paths from u to v using only
    intermediate states from the set/list A (by your convention: A is a
    prefix of [0,1,...,k] and we always remove the last state).
    """

    # Collect all alphabet symbols that realize the single-step transition u -> v
    def symbols_for(u_, v_):
        syms = [alphabet_list[i] for i, dest in enumerate(delta_list[u_]) if dest == v_]
        return " + ".join(syms)

    # Base: no intermediates allowed
    if len(A) == 0:
        syms = symbols_for(u, v)
        if u == v:
            # α_∅(u,u) = (a1 + a2 + ... + ε) if any self-loop symbols; else ε
            return f"({syms} + {epsilon})" if syms else epsilon
        else:
            # α_∅(u,v) = (a1 + a2 + ...) if any direct edges; else ∅
            return f"({syms})" if syms else null

    # Recursive step: remove the last state q in A
    q = A[-1]
    state_step = state_index[len(A) - 1]   # A without q, by your construction

    # α_A(u,v) = α_{A\{q}}(u,v) + α_{A\{q}}(u,q) (α_{A\{q}}(q,q))* α_{A\{q}}(q,v)
    return simplify(
        alpha_construction_step(state_step, u, v),
        alpha_construction_step(state_step, u, q),
        alpha_construction_step(state_step, q, q),
        alpha_construction_step(state_step, q, v),
    )


parts = []
for f in F:
    r = alpha_construction_step(state_index[-1], 0, f)
    if r != null:
        parts.append(r)
regular_expression = " + ".join(parts) if parts else null
print(regular_expression)