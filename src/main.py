from simulator import Simulator
from instructions import InstructionsCache
from memory import Memory
from register import RegisterBank

cache = InstructionsCache('test/build/bin/000.main.bin', 4)
bank = RegisterBank()
memory = Memory()
sim = Simulator(cache, bank, memory)
for i in range(5):
    sim.simulate_cycle()