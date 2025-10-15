# Beckett O'Reilly, River Costello, Johnson Schwede
# CS301 Programming Assignment
# October 13, 2025

epsilon = '\u03B5'
null = '\u2205'

def deep_copy(d):
    out = {}
    for r, row in d.items():
        new_row = {}
        for c, v in row.items():
            new_row[c] = v
        out[r] = new_row
    return out

def parenthesize(x):
    if x in (null, epsilon, ''): return x
    for ch in x:
        if ch in '+()*|':
            return f'({x})'
    return x

def union(a, b):
    if a in (null, ''): return b
    if b in (null, ''): return a
    if a == b: return a
    return f'{a}+{b}'

def concatenation(a, b):
    if null in (a, b): return null
    if a == epsilon: return b
    if b == epsilon: return a
    return a + b

def kleene_star(x):
    if x in (null, epsilon, ''): return epsilon
    return x if x.endswith('*') else f'{parenthesize(x)}*'

class DFA:
    def __init__(self, states, alphabets, init_state, final_states, transition_funct):
        self.states = list(states)
        self.alphabets = list(alphabets)
        self.init_state = init_state
        self.final_states = list(final_states)
        self.transition_funct = transition_funct
        self.ds = {}
        self.seed()

    def seed(self):
        ds = {r: {concatenation: null for concatenation in self.states} for r in self.states}
        for i in self.states:
            nxt = self.transition_funct[i]
            for k, j in enumerate(nxt):
                ds[i][j] = union(ds[i][j], str(self.alphabets[k]))
        self.ds = ds
        self._orig = deep_copy(ds)

    def incoming_states(self, s):
        out = []
        for r, row in self.ds.items():
            if r != s and (s in row) and row[s] != null:
                out.append(r)
        return out

    def outgoing_states(self, s):
        out = []
        for c, v in self.ds[s].items():
            if c != s and v != null:
                out.append(c)
        return out

    def eliminate(self, k):
        Rkk = self.ds[k][k]
        sk = kleene_star(Rkk) if Rkk != '' else epsilon
        for i in self.incoming_states(k):
            Rik = self.ds[i][k]
            for j in self.outgoing_states(k):
                Rkj = self.ds[k][j]
                self.ds[i][j] = union(self.ds[i][j], concatenation(concatenation(parenthesize(Rik), sk), parenthesize(Rkj)))
        # remove k
        self.ds = {r: {concatenation: v for concatenation, v in row.items() if concatenation != k} for r, row in self.ds.items() if r != k}
        self.states = [kleene_star for kleene_star in self.states if kleene_star != k]

    def convert(self):
        # Start from the original adjacency
        base = deep_copy(self._orig)
        base_states = list(base.keys())

        # Pick fresh names for super start/accept
        S0, T0 = '__S__', '__T__'
        while S0 in base_states or T0 in base_states:
            S0, T0 = '_' + S0, '_' + T0

        # Build GNFA matrix with S0 and T0
        self.states = [S0] + base_states + [T0]
        self.ds = {r: {concatenation: null for concatenation in self.states} for r in self.states}
        # copy original edges
        for r in base_states:
            for concatenation in base_states:
                self.ds[r][concatenation] = base[r][concatenation]
        # ε from S0 to init
        self.ds[S0][self.init_state] = union(self.ds[S0][self.init_state], epsilon)
        # ε from each final to T0
        for f in self.final_states:
            self.ds[f][T0] = union(self.ds[f][T0], epsilon)
        # if init is final, allow ε directly S0->T0 (empty path)
        if self.init_state in self.final_states:
            self.ds[S0][T0] = union(self.ds[S0][T0], epsilon)

        # Eliminate everything except S0 and T0
        for k in list(self.states):
            if k not in (S0, T0):
                self.eliminate(k)

        # Resulting regex is the single edge S0->T0
        return self.ds[S0][T0]

def main():
    alph = list(input("Enter alphabet elements. Exclude all brackets, commas, and spaces. "))
    delta_int, delta_str, kleene_star = [], [], 0
    while True:
        row = input(f"Enter transition function for state {kleene_star}. Exclude all brackets, commas, and spaces. ").strip()
        if len(row) != len(alph): row = (row + '0'*len(alph))[:len(alph)]
        ints = [int(ch) for ch in row]; delta_int.append(ints); delta_str.append([str(x) for x in ints])
        kleene_star += 1
        if input("Enter another state? (y/n) ").strip().lower() != 'y': break
    Fs = input("Enter accepting states. Exclude all brackets, commas, and spaces. ").strip()
    F_int = [int(ch) for ch in Fs] if Fs else []
    states = [str(i) for i in range(len(delta_str))]
    trans = {states[i]: delta_str[i] for i in range(len(states))}
    print(f"Alphabet: {alph}, Delta: {delta_int}, F: {F_int}")
    if not F_int: print(null); return
    dfa = DFA(states, alph, "0", [str(x) for x in F_int], trans)
    print(dfa.convert())

if __name__ == '__main__':
    main()