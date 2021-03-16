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
    [gen_1234(i) for i in range(1, 5)] # 单牌、对牌、三张、炸弹
    + [gen_rocket] # 火箭
    + [gen_seq_123(1)]*8 # 连单
    + [gen_seq_123(2)]*8 # 连对
    + [gen_seq_123(3)]*5 # 连三
    + [gen_tri_12345_with_12(i, j) for i in range(1, 5) for j in range(1, 3)] # 连三带单、对
    + [gen_tri_12345_with_12(5, 1)] # 连5个三带单
    + [gen_quad_with(1)] # 四带两单
    + [gen_quad_with(2)] # 四带两对
)

# 牌组减法
def minus(base, comb):
    return [i-j for i,j in zip(base, comb)]

# base去掉comb中含有的牌，并且防止产生所带的牌和飞机连续
def minus_all(base, comb):
    # 三头（含）
    s = comb.index(3)
    # 三尾（不含）
    e = 15 - comb[::-1].index(3)
    # 除去base中含有comb的牌，防止出现炸弹
    new_base = base[:s]+[0]*(e-s)+base[e:]
    # 除去base中含有的炸弹，防止出现炸弹
    new_base = [i if i < 4 else 3 for i in new_base]
    # 如果被带的牌中可能在三连之前且与三连构成更大的飞机
    # 例如 444355536663 => 333444555666，应当禁止
    if s > 0 and new_base[s-1] > 2:
        new_base[s-1] = 2
    # 如果在三连之后可能构成更大的飞机(e不含)，不允许，最多允许用两张该牌
    if e < 12 and new_base[e] > 2:
        new_base[e] = 2
    return new_base

# 牌组加法
def add(comb1, comb2):
    return [i+j for i,j in zip(comb1, comb2)]

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
            # 从card_s+i的后一位(card_s+i+1)开始看是否有可用连牌
            for j in range(card_s+i+1, card_e+i+2):
                if useable_card[j] < k:
                    break
            else:
                yield [0]*(card_s+i+1) + [k]*(card_e-card_s+1) + [0]*(13-card_e-i)
    return gen_seq_k

# 以下需要根据竞技二打一比赛规则调整：
# 飞机不能含有炸弹、火箭，也不能带与飞机相连续的三张牌

# 生成三带所用单牌
def gen_singles(n, useable_card, s=0, record=[0]*15):
    if n == 0:
        # 所带的牌中不能有火箭
        if record[13]==0 or record[14]==0:
            yield record
        return
    # 如果选牌选到了最后一张，还没有选够
    if s == 15 or sum(useable_card[s:]) < n:
        return
    # s处可用的单牌数
    useable = min(useable_card[s], n)
    for i in range(0, useable+1):
        yield from gen_singles(n-i, useable_card, s+1, record[:s]+[i]+record[s+1:])
    
# 生成三带所用对牌
def gen_pairs(n, useable_card, s=0, record=[0]*15):
    if n == 0:
        yield record
        return
    if s == 13 or sum(useable_card[s:]) < n*2:
        return
    # s处可用的对牌数
    useable = min(useable_card[s]//2, n)
    for i in range(0, useable+1):
        yield from gen_pairs(n-i, useable_card, s+1, record[:s]+[2*i]+record[s+1:])
    
# 生成（连1-5）三带一、对
def gen_tri_12345_with_12(n, m):
    def gen_tri_k_with_l(useable_card, k=n, l=m, base_card=None):
        # 如果牌不够，没法出
        if sum(useable_card) < n*(3+l):
            return
        # 需要压制的牌从哪开始三带
        base_s = -1 if not base_card else base_card.index(3)
        # 生成三连，可用的牌必须起点比需要压制的牌高
        for tri in (gen_1234 if k==1 else gen_seq_123)(3)(
            useable_card=[0]*base_s+useable_card[base_s+1:]):
            # 可用于带的牌
            left = minus_all(useable_card, tri)
            # 生成带的牌组
            for w in {1:gen_singles, 2:gen_pairs}[l](k, useable_card=left):
                yield add(tri, w)
    return gen_tri_k_with_l

# 生成四带两单、两对
def gen_quad_with(n):
    def gen_quad_with_k(useable_card, k=n, base_card=None):
        # 如果牌不够，生成不了
        if sum(useable_card) < 4+2*n:
            return
        base_s = -1 if not base_card else base_card.index(4)
        for quad in gen_1234(4)(
            useable_card=[0]*base_s+useable_card[base_s+1:]):
            left = minus_all(useable_card, quad)
            for w in {1:gen_singles, 2:gen_pairs}[2](k, useable_card=left):
                yield add(tri, w)
    return gen_quad_with_k


initial_state = {
    'turn':0,
    'card':[[],[],[]],
    'last':{'turn':0, 'card':None, 'type':None}
}

# 根据需要压制的出牌类型生成能压制其的牌
def gen_comb_above(base_card_type=None, useable_card):
    # 如果是首次出牌或者无人压制再次轮到，不能过牌，只能出
    if not base_card_type:
        # 尝试所有的可能出牌种类（单、对、三、炸、带、连）
        for k, v in card_type.items():
            # 枚举该出牌类型下的所有可能出牌方式
            for comb in gen_combs_of[v](useable_card=useable_card):
                # 返回牌组、类型
                yield comb, card_type[k]
    else:
        # 上家出牌后，可以选择过牌，类型为空
        yield [0]*15, None 
        # 如果是为了压制上家牌（出同种更大的）
        for comb in gen_combs_of[base_card_type['type']](
            base_card_type=base_card_type['card'], useable_card=useable_card):
            yield comb, base_card_type['type']
        # 如果上家出的不是炸弹或者火箭，可以尝试出炸弹压制
        # （如果上家是炸弹，则已经在上一步被压制了）
        if base_card_type['type'] not in {card_type['B'], card_type['R']}:
            for comb in gen_combs_of[card_type['B']](useable_card=useable_card):
                yield comb, card_type['B']
        # 如果上家出的不是火箭，尝试出火箭压制
        if base_card_type['type'] != card_type['R']:
            for comb in gen_combs_of[card_type['R']](useable_card=useable_card):
                yield comb, card_type['R']

# 完美信息牌局模拟
def play(state):
    # 当前应该出牌的玩家
    curr = state['turn']
    # 当前待出牌玩家可用的牌
    useable_card = state['card'][curr]
    # 未被压制的上家
    last = state['last']['turn'] 
    # 未被压制的上家牌+上家牌类型
    base_card_type = state['last']
    # 未被压制的上家牌
    base_card = base_card_type['card']
    # 如果本家上一轮所出的牌无人压制
    if curr == last:
        # 清空待压制牌
        base_card_type = None
    # 尝试出牌压制上家（如果没有上家，则遍历所有出牌方式）
    for comb, comb_type in gen_comb_above(
        base_card_type=base_card_type, useable_card=useable_card):
        # 输出玩家号（0=地主，1=农民1，2=农民2）
        print(curr, comb)
        # 状态转移
        next_state = {
            # 轮到下家出牌
            'turn':(curr+1)%3,
            # 仅本家牌减少
            'card':(state['card'][:curr] 
                + minus(useable_card, comb) 
                + state['card'][curr+1:]
            ),
            # 如果本家没有过牌（comb_type不为空），则待下家压制的牌为本家所出，否则待压制牌不变
            'last':({'turn':curr, 'card':comb, 'type':comb_type} 
                if comb_type else base_card_type
            )
        }
        # 如果本家牌清空，本家胜
        if sum(next_state['card'][curr]) == 0:
            return curr
        # 否则递归模拟所有分支
        play(next_state)