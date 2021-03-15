'''
def gen_1234(n):
    # k=n表示牌的张数(1,2,3,4)
    def gen_k(useable_card, k=n, base_card=None):
        # 如果是开牌
        if not base_card:
            card = -1
        else:
            card = base_card.index(k)
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
f = gen_1234(1)
for i in f(useable_card=[2,3,4,2,3,
                         2,2,0,1,2,
                         3,0,0,0,1], base_card=[0,0,0,0,0,
                                                1,0,0,0,0,
                                                0,0,0,0,0]):
    print(i)
'''
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

g = gen_seq_123(3)

for i in g(useable_card=[2,1,1,3,4,
                         3,2,2,1,2,
                         3,3,2,1,0], base_card=[0,0,3,3,0,
                                                0,0,0,0,0,
                                                0,0,0,0,0]):
    print(i)
    print(i)
