# -*- coding: utf-8 -*-

import inspect

class Channel(object):
    def __init__(self):
        self.state = '0'
        self.proof = []


    def send(self, s):
        self.state = sha256((self.state + s).encode()).hexdigest()
        self.proof.append(f'{inspect.stack()[0][3]}:{s}')


    def receive_random_int(self, min, max, show_in_proof=True):
        pass
