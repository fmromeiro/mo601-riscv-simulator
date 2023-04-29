import os
import traceback
from simulator import Simulator
from instructions import InstructionsCache
from memory import Memory
from register import RegisterBank

def find_tests() -> [os.DirEntry]:
    return sorted([test for test in os.scandir('./test/build/bin') if test.name.endswith('.bin')], key= lambda x: x.name)

def run_test(file: os.DirEntry):
    bank = RegisterBank()
    memory = Memory()
    cache = InstructionsCache(file.path, 4, memory)
    with open(os.path.join('test/', file.name[:-4] + '.log'), 'tw') as log:
        sim = Simulator(cache, bank, memory, log)
        sim.simulate()



if __name__ == '__main__':
    for test in find_tests():
        try:
            run_test(test)
        except:
            print(f'Error while running test {test.name}:')
            print(traceback.format_exc())
            input()