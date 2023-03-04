### TEAM MEMBERS
## MEMBER 1: 210050018
## MEMBER 2: 210050038
## MEMBER 3: 210050085

from z3 import *
import sys

if (len(sys.argv) != 2):
    print(f"Usage: {sys.argv[0]} <input_file>")
    sys.exit(0)
with open(sys.argv[1]) as f:
    n,T = [int(x) for x in next(f).split()]
    matrix = []

    for line in f:
        matrix.append([int(x) for x in line.split()])

# Set s to the required formula
s = Solver()

v = []
moves = []
for k in range(T + 1):
    T1 = []
    for i in range(n):
        T2 = []
        for j in range(n):
            T2.append(Int(f'{k}_{i}_{j}'))
        T1.append(T2[:])
    v.append(T1)

for k in range(0, T):
    # 0->u, 1->d, 2->l, 3->r
    # move = 4 * index + (u|d|l|r)
    moves.append(Int(f'move_{k}'))
    s.add(moves[-1] >= 0, moves[-1] < 4 * n)

end = [True] * (T + 1)
finished = [Bool(f'finished_{k}') for k in range(T + 1)]
for i in range(n):
    for j in range(n):
        s.add(v[0][i][j] == matrix[i][j])
        for k in range(T + 1):
            end[k] = And(end[k], v[k][i][j] == n*i+j+1)

for k in range(T + 1):
    s.add(finished[k] == end[k])

s.add(Or(*tuple(end)))

for k in range(T - 1):
    for j in range(n):
        for w in range(n):
            # left
            s.add(Implies(And(moves[k] % 4 == 0, moves[k] / 4 == w), And(v[k][j][w] == v[k + 1][(j - 1) % n][w], Implies(Or(moves[k + 1] % 4 == 0, moves[k + 1] % 4 == 1), moves[k + 1] / 4 >= w))))
            # right
            s.add(Implies(And(moves[k] % 4 == 1, moves[k] / 4 == w),  And(v[k][j][w] == v[k + 1][(j + 1) % n][w], Implies(Or(moves[k + 1] % 4 == 0, moves[k + 1] % 4 == 1), moves[k + 1] / 4 >= w))))
            # up
            s.add(Implies(And(moves[k] % 4 == 2, moves[k] / 4 == w), And(v[k][w][j] == v[k + 1][w][(j - 1) % n], Implies(Or(moves[k + 1] % 4 == 2, moves[k + 1] % 4 == 3), moves[k + 1] / 4 >= w))))
            # down
            s.add(Implies(And(moves[k] % 4 == 3, moves[k] / 4 == w), And(v[k][w][j] == v[k + 1][w][(j + 1) % n], Implies(Or(moves[k + 1] % 4 == 2, moves[k + 1] % 4 == 3), moves[k + 1] / 4 >= w))))
            
            # left/right unmodified rows
            s.add(Implies(And(Or(moves[k] % 4 == 0, moves[k] % 4 == 1), moves[k] / 4 != w), v[k][j][w] == v[k + 1][j][w]))
            # up/down unmodified columns
            s.add(Implies(And(Or(moves[k] % 4 == 2, moves[k] % 4 == 3), moves[k] / 4 != w), v[k][w][j] == v[k + 1][w][j]))

for j in range(n):
    for w in range(n):
	    # left
        s.add(Implies(And(moves[T - 1] % 4 == 0, moves[T - 1] / 4 == w), v[T - 1][j][w] == v[T - 1 + 1][(j - 1) % n][w]))
        # right
        s.add(Implies(And(moves[T - 1] % 4 == 1, moves[T - 1] / 4 == w),  v[T - 1][j][w] == v[T - 1 + 1][(j + 1) % n][w]))
        # up
        s.add(Implies(And(moves[T - 1] % 4 == 2, moves[T - 1] / 4 == w), v[T - 1][w][j] == v[T - 1 + 1][w][(j - 1) % n]))
        # down
        s.add(Implies(And(moves[T - 1] % 4 == 3, moves[T - 1] / 4 == w), v[T - 1][w][j] == v[T - 1 + 1][w][(j + 1) % n]))
        
        # left/right unmodified rows
        s.add(Implies(And(Or(moves[T - 1] % 4 == 0, moves[T - 1] % 4 == 1), moves[T - 1] / 4 != w), v[T - 1][j][w] == v[T - 1 + 1][j][w]))
        # up/down unmodified columns
        s.add(Implies(And(Or(moves[T - 1] % 4 == 2, moves[T - 1] % 4 == 3), moves[T - 1] / 4 != w), v[T - 1][w][j] == v[T - 1 + 1][w][j]))

x = s.check()
print(x)

if x == sat:
    MNAMES = 'udlr'
    m = s.model()
    # Output the moves
    total_moves = 0
    for k in range(T + 1):
        if (m[finished[k]]):
            total_moves = k
            break
    output = []
    for k in range(total_moves):
        x = m[moves[k]].as_long()
        output.append((x // 4, x % 4))
    i = 1
    while (i < len(output)):
        if (output[i - 1][0] == output[i][0] and ((output[i - 1][1] + output[i][1]) % 4 == 1)):
            output = output[:i - 1] + output[i + 1:]
            if (i >= 2):
                i -= 2
                continue
        i += 1
    for m in output:
        print(m[0], MNAMES[m[1]], sep='')
