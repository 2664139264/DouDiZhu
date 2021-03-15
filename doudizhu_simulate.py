card = [
    '3','4','5','6','7','8','9','10','J','Q','K','A', # 0-11 可连
    '2', # 12 不可连，可比
    'joker','JOKER' # 13-14 可单出，可成火箭
]
card_type = {
    '1':0, '2':1, '3':2, # 单牌、对牌、三张
    'B':3, 'R':4, # 炸弹、火箭
    '1-5':5, '1-6':6, '1-7':7, '1-8':8, '1-9':9, '1-10':10, '1-11':11, '1-12':12, # 单连-长度
    '2-3':13, '2-4':14, '2-5':15, '2-6':16, '2-7':17, '2-8':18, '2-9':19, '2-10':20, # 连对-长度
    '3-2':21, '3-3':22, '3-4':23, '3-5':24, '3-6':25, # 三连-长度
    '3+1':26, '3+2':27, # 三带+单/对
    '3-2+1':28, '3-2+2':29, # 飞机2+单/对
    '3-3+1':30, '3-3+2':31, # 飞机3+单/对
    '3-4+1':32, '3-4+2':33, # 飞机4+单/对
    '3-5+1':34, # 飞机5+单
    '4+1+1':35, '4+2+2':36, # 四带+2单/2对
}
gen_combs_of = (
    [gen_1234(i) for i in range(1, 5)] # 单牌、对牌、三张、四张
    + [gen_rocket] # 火箭
    + [gen_seq_123(1)]*8 # 连单
    + [gen_seq_123(2)]*8 # 连对
    + [gen_seq_123(3)]*5 # 连三
    + [gen_tri_12345_with_12(i, j) for i in range(1, 5) for j in range(1, 3)] # 连三带单、对
    + [gen_tri_12345_with_12(5, 1)] # 连5个三带单
    + [gen_quad_with_1_1] # 四带两单
    + [gen_quad_with_2_2] # 四带两对
)
# 生成1,2,3,4张大小相同的牌
def gen_1234(n):
    # k=n表示牌的张数(1,2,3,4)
    def gen_k(useable_card, k=n, base_card=None):
        # 如果是开牌
        if not base_card:
            # 任意一种都可以
            card = -1
        else:
            # 否则需要大于上家牌
            card = base_card.index(k)
        # 始终可以出的：3-A, 2
        for i in range(card+1, 13):
            if useable_card[i] >= k:
                yield [0]*i+[k]+[0]*(15-i-1)
        # 如果是单牌，考虑用Joker
        if k == 1:
            if useable_card[13] > 0:
                yield [0]*13+[1,0]
            if useable_card[14] > 0:
                yield [0]*14+[1]
    return gen_k

# 生成火箭牌
def gen_rocket(useable_card):
    if useable_card[13] > 0 and useable_card[14] > 0:
        yield [0]*13+[1,1]

# 生成连单、连对、连三
def gen_seq_123(n):
    def gen_seq_k(useable_card, k=n, base_card=None):
        # 如果是开牌
        if not base_card:
            # 枚举连牌长度
            for l in range({1:5,2:3,3:2}[k], {1:12, 2:10, 3:6}[k]+1):
                # 枚举连牌开始，范围从s到e（不含）
                s, e = 0, 13-l
                while s < e:
                    # 如果该处有可用的足够多的牌
                    if useable_card[s] >= k:
                        # 检查从此开始长度为l的k序列是否存在
                        for ss in range(s+1, s+l):
                            if useable_card[ss] < k:
                                # 如果在ss处中断，把s调整到ss继续检查
                                s = ss
                                break
                        else:
                            yield [0]*s+[k]*l+[0]*(15-s-l)
                    s += 1
            return
        # 如果有需要压制的牌，计算牌总数
        cnt_usable_card = sum(useable_card)
        cnt_base_card = sum(base_card)
        # 如果牌不够，那自然打不过
        if cnt_base_card > cnt_usable_card:
            return
        # 对方连牌开始
        card_s = base_card.index(k)
        # 对方连牌结束（含）
        card_e = 14-base_card[::-1].index(k)
        # 最多11-card_e步，如果对方连到card[11]: 'A'，则无可前进空间
        max_step = 11 - card_e
        for i in range(0, max_step):
            # 从card_s+i的后一位开始看是否有可用连牌
            for j in range(card_s+i+1, card_e+i+2):
                if useable_card[j] < k:
                    break
            else:
                yield [0]*(card_s+i+1) + [k]*(card_e-card_s+1) + [0]*(13-card_e-i)
    return gen_seq_k

# 生成（连1-5）三带一、对
def gen_tri_12345_with_12(n, m):
    def gen_tri_n_with_m(useable_card, k=n, l=m, base_card=None):
        if not base_card:
            
            return
        cnt_usable_card = sum(useable_card)
        cnt_base_card = sum(base_card)
        if cnt_base_card > cnt_usable_card:
            return
        card_s = base_card.index(3)
        card_e = 14-base_card[::-1].index(3)

    
    return gen_tri_n_with_m


initial_state = {
    'turn':0,
    'card':[[],[],[]],
    'last':{'turn':0, 'card':None, 'type':None}
}

# 根据需要压制的出牌类型生成能压制其的牌
def gen_comb_above(base_card=None, useable_card):
    # 如果是首次出牌或者无人压制再次轮到
    if not base_card:
        # 尝试所有的可能出牌种类（单、对、三、炸、带、连）
        for k, v in card_type.items():
            # 枚举该出牌类型下的所有可能出牌方式
            for comb in gen_combs_of[v](useable_card=useable_card):
                yield comb, card_type[k]
    else:
        yield [0]*15, None # 可以选择过牌
        for comb in gen_combs_of[base_card['type']](
            base_card=base_card['card'], useable_card=useable_card):
            yield comb, base_card['type']
        if base_card['type'] != card_type['B']:
            for comb in gen_combs_of[card_type['B']](useable_card=useable_card):
                yield comb, card_type['B']
        if base_card['type'] != card_type['R']:
            for comb in gen_combs_of[card_type['R']](useable_card=useable_card):
                yield comb, card_type['R']
        
        
def minus(base, comb):
    return [i-j for i,j in zip(base, comb)]

def play(state):
    curr = state['turn'] # 当前应该出牌的玩家
    useable_card = state['card'][curr] # 当前待出牌玩家可用的牌
    last = state['last']['turn'] # 上一个未被压制的出牌者
    base_card = state['last']
    if curr == last:
        base_card = None
    for comb, comb_type in gen_comb_above(
        base_card=base_card, useable_card=useable_card):
        print(curr, comb)
        next_state = {
            'turn':(curr+1)%3,
            'card':(state['card'][:curr] 
                + minus(state['card'][curr], comb) 
                + state['card'][curr+1:]
            ),
            'last':({'turn':curr, 'card':comb, 'type':comb_type} 
                if comb_type else state['last']
            )
        }
        if sum(next_state['card'][curr]) == 0:
            return curr
        play(next_state)