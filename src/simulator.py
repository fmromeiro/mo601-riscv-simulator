from instructions import InstructionsCache
from register import RegisterBank
from memory import Memory
from utils import *

class Simulator:
    _signals = dict

    def __init__(self, instructions_cache: InstructionsCache, register_bank: RegisterBank, memory: Memory):
        self._instructions_cache = instructions_cache
        self._register_bank = register_bank
        self._memory = memory
        self._signals = {'is_branch': True, 'branch_addr': 0}

    def instruction_fetch(self) -> int:
        if self._signals['is_branch']:
            instr = self._signals['branch_addr']
        else:
            pc = self._register_bank.get_register('pc')
            instr = pc + 4
        self._register_bank.set_register('pc', instr)
        return self._instructions_cache.load_instruction(instr)

    def instruction_decode(self, instruction: int) -> dict[str, int]:
        rd = to_uint(slice_instruction(instruction, 7, 11))
        rs1 = to_uint(slice_instruction(instruction, 15, 19))
        rs2 = to_uint(slice_instruction(instruction, 20, 24))
        rs1_value = self._register_bank.get_register(rs1)
        rs2_value = self._register_bank.get_register(rs2)

        opcode = slice_instruction(instruction, 0, 6)
        imm = 0
        name = ""
        match opcode:
            case 55:
                name = 'LUI'
                imm = to_uint(slice_instruction(instruction, 12, 31))
            case 23:
                name = 'AUIPC'
                imm = to_uint(slice_instruction(instruction, 12, 31))
            case 111:
                name = 'JAL'
                imm = slice_instruction(instruction, 21, 30)
                imm = slice_instruction(instruction, 20, 20) + imm
                imm = slice_instruction(instruction, 12, 19) + imm
                imm = slice_instruction(instruction, 31, 31) + imm

    def simulate_cycle(self):
        print(self.instruction_fetch())
        self._signals.update({'is_branch': False})
