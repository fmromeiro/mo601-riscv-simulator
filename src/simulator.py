from instructions import InstructionsCache
from register import RegisterBank
from memory import Memory
import decoder
from utils import *

class Simulator:
    def __init__(self, instructions_cache: InstructionsCache, register_bank: RegisterBank, memory: Memory, log_file):
        self._instructions_cache = instructions_cache
        self._register_bank = register_bank
        self._memory = memory
        self.decoder = decoder.Decoder(register_bank, memory)
        self.log = log_file

    def instruction_fetch(self) -> decoder.Instruction:
        instr = self._instructions_cache.load_instruction(self._register_bank.get_register('pc'))
        return self.decoder.build_instruction(instr)

    def simulate_cycle(self) -> bool:
        instr = self.instruction_fetch()
        instr.exec()
        self.log.write(instr.log() + '\n')
        return not instr.is_end()

    def simulate(self):
        while self.simulate_cycle():
            pass