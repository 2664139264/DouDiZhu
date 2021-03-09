card = ['A','2','3','4','5','6','7','8','9','10','J','Q','K','joker','JOKER']
card_rep = [4,4,4,4,4,4,4,4,4,4,4,4,4,1,1]

def gen_alloc3(n):
    for i in range(n+1):
        for j in range(n-i+1):
            yield (i, j, n-i-j)

def add(tr1, tr2):
    return tuple([i+j for i,j in zip(tr1, tr2)])

def calc_init(card_rep):
    card_type = len(card_rep)
    A = {-1: {(0,0,0):1}}
    for i in range(card_type):
        A[i] = dict()
        for alloc_vec in gen_alloc3(card_rep[i]):
            for k, v in A[i-1].items():
                new_alloc_vec = add(k, alloc_vec) 
                A[i][new_alloc_vec] = v + (
                    A[i][new_alloc_vec] if new_alloc_vec in A[i].keys() else 0)
    return A


print(calc_init(card_rep)[14][(20,17,17)])

joker0 = (13 * calc_init([1]+card_rep[1:])[14][(17,17,17)] + 
    156 * calc_init([2, 3]+card_rep[2:])[14][(17,17,17)])

joker1 = (26 * calc_init([2]+card_rep[1:-1])[13][(17,17,17)] + 
    156 * calc_init([3,3]+card_rep[2:-1])[13][(17,17,17)])

joker2 = 13 * calc_init([3]+card_rep[1:-2])[12][(17,17,17)]
print(joker0+joker1+joker2)

