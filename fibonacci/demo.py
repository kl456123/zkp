# -*- coding: utf-8 -*-


from field import FieldElement
from polynomial import X, interpolate_poly
from merkle import MerkleTree
from channel import Channel
import time


a = [FieldElement(1), FieldElement(3141592)]
channel = Channel()

def testing_trace():
    while len(a) < 1023:
        a.append(a[-2]* a[-2] + a[-1]* a[-1])

    # test trace of a
    assert len(a) == 1023
    assert a[0] == FieldElement(1), 'The first element in the trace must be the unit element'
    for i in range(2, 1023):
        assert a[i] == a[i-1]*a[i-1] + a[i-2] * a[i-2], f'{i}'
    assert a[1022] == FieldElement(2338775057)
    print('Success')


def testing_LDE():
    # generate
    g = FieldElement.generator()**(3*2**20)
    G = [g**i for i in range(1024)]
    # tmp = FieldElement(5**(3*2**30))
    print(G)

    # testing
    assert g.is_order(1024)
    b = FieldElement(1)
    for i in range(1023):
        assert b == G[i]
        b = b*g
        assert b!=FieldElement(1)

    if b* g == FieldElement(1):
        print('Success')
    else:
        print('g is of order > 1024')

def testing_polynomial():
    p = 2*X**2+1
    print(p(2))

    # interpolation
    f = interpolate_poly(G[:-1], a)
    v = f(2)

    assert v == FieldElement(1302089273)
    print('Success')

    # extend domain of G to H
    w = FieldElement.generator()
    h = w ** ((2 ** 30* 3)//8192)
    H = [h**i for i in range(8192)]
    # shift it by the generator w
    eval_domain = [w * x for x in H]

    f_eval = [f(d) for d in eval_domain]

    f_merkle = MerkleTree(f_eval)
    assert f_merkle.root == '6c266a104eeaceae93c14ad799ce595ec8c2764359d7ad1b4b7c57a4da52be04'
    print('Success')

    channel.send(f_merkle.root)
    print(channel.proof)


def get_CP(channel, p):
    [p0, p1, p2] = p
    alpha0 = channel.receive_random_field_element()
    alpha1 = channel.receive_random_field_element()
    alpha2 = channel.receive_random_field_element()
    return alpha0*p0+alpha1*p1+alpha2*p2


def testing_contraits():
    # 1.
    numer0 = f-1
    denum0 = X-1
    p0 = numer0 / denum0

    # 2.
    numer1 = f - 2338775057
    denum1 = X- g**1022
    p1 = numer1 / denum1

    # 3.
    numer2 = f(g**2*X) - f(g*X) ** 2 - f**2
    denum2 = (X**1024-1)/ ((X - g**1021) * (X-g**1022)*(X-g**1023))
    p2 = numer2 / denum2

    # compose them in all
    CP = get_CP(channel)
    CP_merkle = MerkleTree([CP[d] for d in eval_domain])
    channel.send(CP_merkle.root)


##############################
###### FRI Operator

def next_fri_domain(fri_domain):
    return [x** 2 for x in fri_domain[: len(fri_domain)//2]]

def next_fri_polynomial(poly, beta):
    odd_coefficients = poly.poly[1::2]
    even_coefficients = poly.poly[::2]
    odd = beta * Polynomial(odd_coefficients)
    even = Polynomial(even_coefficients)
    return even + odd

def next_fri_layer(poly, domain, beta):
    next_poly = next_fri_polynomial(poly, beta)
    next_domain = next_fri_domain(domain)
    next_layer = [next_poly(x) for x in next_domain]
    return next_poly, next_domain, next_layer


def FriCommit(cp, domain, cp_eval, cp_merkle, channel):
    fri_polys = [cp]
    fri_domain = [domain]
    fri_layers = [cp_eval]
    fri_merkles = [cp_merkle]
    while fri_polys[-1].degree()>0:
        beta = channel.receive_random_field_element()
        next_poly, next_domain, next_layer = next_fri_layer(
            fri_polys[-1], fri_domain[-1], beta)
        fri_polys.append(next_poly)
        fri_domain.append(next_domain)
        fir_layers.append(next_layer)
        fri_merkles.append(MerkleTree(next_layer))
        channel.send(fri_merkles[-1].root)
    # send constant to verifier
    channel.send(str(fri_polys[-1].poly[0]))
    return fri_polys, fri_domain, fri_layers, fri_merkles

#############################
## Decommit Phase

def decommit_on_fri_layers(idx, channel):
    for layer, merkle in zip(fri_layers[:-1], fri_merkles[:-1]):
        length = len(layer)
        idx = idx%length
        sib_idx = (idx+length//2)%length
        channel.send(str(layer[idx]))
        channel.send(str(merkle.get_authentication_path(idx)))
        channel.send(str(layer[sib_idx]))
        channel.send(str(merkle.get_authentication_path(sib_idx)))
    channel.send(str(fri_layers[-1][0]))




def decommit_on_query(idx, channel):
    assert idx + 16 < len(f_eval),
    f'query index: {idx} is out of range. Length of layer: {len(f_eval)}.'
    channel.send(str(f_eval[idx]))
    channel.send(str(f_merkle.get_authentication_path(idx)))
    channel.send(str(f_eval[idx+8]))
    channel.send(str(f_merkle.get_authentication_path(idx+8)))
    channel.send(str(f_eval[idx+16]))
    channel.send(str(f_merkle.get_authentication_path(idx+16)))
    decommit_on_fri_layers(idx, channel)

def decommit_fri():
    for query in range(3):
        decommit_on_query(channel.receive_random_int(0, 8191-16), channel)


def prove():
    start = time.time()
    # generate trace

    # generate composition polynomial

    # generate fri layers

    # generate queries and decommitments






if __name__=='__main__':
    # testing_LDE()

    testing_polynomial()
