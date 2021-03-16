from doudizhu_simulate import *

'''
f = gen_tri_12345_with_12(3, 2)
for s in f(useable_card=[3,3,3,4,1,
                         2,3,2,1,1,
                         1,3,1,1,1],
           base_card=[3,3,3,0,0,
                      0,2,2,0,2,
                      0,0,0,0,0]):
    print(s)
f = gen_quad_with(1)
for s in f(useable_card=[1,0,0,0,4,
                         4,0,0,3,2,
                         2,0,0,1,1],
           base_card=[0,0,4,0,0,
                      0,0,0,0,0,
                      2,0,2,0,0]):
       print(s)
'''

initial_state = {
    'turn':0,
    'card':[[3,0,0,0,0,
             0,4,0,0,0,
             0,0,0,0,0],[0,0,0,3,4,
                         0,0,0,0,0,
                         0,0,0,0,0],[0,0,0,0,0,
                                     0,0,0,0,0,
                                     0,0,0,0,0]],
    'last':{'turn':0, 'card':None, 'type':None}
}
for c in initial_state['card']:
    print(f"init: {wrapper(c)}")
play(initial_state)

