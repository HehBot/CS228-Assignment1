### TEAM MEMBERS
## MEMBER 1: 210050018
## MEMBER 2: 210050038
## MEMBER 3: 210050085

from z3 import *
import sys

file = sys.argv[1]

with open(file) as f:
    n,T = [int(x) for x in next(f).split()]
    matrix = []

    for line in f:
        matrix.append([int(x) for x in line.split()])

# Set s to the required formula
s = Solver()

v = []
moves = []
for k in range(0, T + 1):
    T1 = []
    for i in range(0, n):
        T2 = []
        for j in range(0, n):
            T2.append(Int(str(k) + '_' + str(i) + '_' + str(j)))
        T1.append(T2[:])
    v.append(T1)

for k in range(0, T):
    # 0->u, 1->d, 2->l, 3->r
    # move = 4 * index + (u|d|l|r)
    moves.append(Int(f'move_{k}'))
    s.add(moves[-1] >= 0, moves[-1] < 4 * n)

x1=True
x2=True
for i in range(0, n):
    for j in range(0, n):
        s.add(v[0][i][j] == matrix[i][j])
        x1 = And(x1, v[T-1][i][j] == n*i+j+1)
        x2 = And(x2, v[T][i][j] == n*i+j+1)

s.add(Or(x1, x2))

for k in range(0, T):
    for j in range(0, n):
        for w in range(0, n):
            s.add(Implies(And(moves[k] % 4 == 0, moves[k] / 4 == w), v[k][j][w] == v[k + 1][(j - 1) % n][w]))
            s.add(Implies(And(moves[k] % 4 == 1, moves[k] / 4 == w), v[k][j][w] == v[k + 1][(j + 1) % n][w]))
            s.add(Implies(And(moves[k] % 4 == 2, moves[k] / 4 == w), v[k][w][j] == v[k + 1][w][(j - 1) % n]))
            s.add(Implies(And(moves[k] % 4 == 3, moves[k] / 4 == w), v[k][w][j] == v[k + 1][w][(j + 1) % n]))
            
            s.add(Implies(And(Or(moves[k] % 4 == 0, moves[k] % 4 == 1), moves[k] / 4 != w), v[k][j][w] == v[k + 1][j][w]))
            s.add(Implies(And(Or(moves[k] % 4 == 2, moves[k] % 4 == 3), moves[k] / 4 != w), v[k][w][j] == v[k + 1][w][j]))

x = s.check()
print(x)

if x == sat:
    MNAMES = 'udlr'
    m = s.model()
    # Output the moves
    for k in range(0, T):
        x = m[moves[k]].as_long()
        print(x // 4, MNAMES[x % 4], sep='')
