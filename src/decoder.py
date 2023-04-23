from register import RegisterBank
from memory import Memory
from instructions import InstructionsCache
from utils import *


class Instruction:
    _instr: str
    _register_bank: RegisterBank
    _memory: Memory
    _rs1_value: int
    _rs2_value: int
    _pc: int

    def __init__(self, instruction: str, register_bank: RegisterBank, memory: Memory):
        self._instr = instruction
        self._register_bank = register_bank
        self._memory = memory
        self._rs1_value = register_bank.get_register(self.get_rs1())
        self._rs2_value = register_bank.get_register(self.get_rs2())
        self._pc = register_bank.get_register('pc')

    def get_rd(self) -> int:
        return to_uint(slice_instruction(self._instr, 7, 11))

    def get_rs1(self) -> int:
        return to_uint(slice_instruction(self._instr, 15, 19))

    def get_rs2(self) -> int:
        return to_uint(slice_instruction(self._instr, 20, 24))

    def get_opcode(self) -> str:
        return slice_instruction(self._instr, 0, 6)

    def _bump_pc(self):
        self._register_bank.set_register('pc', self._pc + 4)

    def get_imm(self) -> int:
        raise NotImplementedError()

    def exec(self):
        raise NotImplementedError()

    def mnem(self):
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()

    def log(self):
        rd = self._register_bank.get_register(self.get_rd())
        instr = int(self._instr, 2)
        res = f'PC={self._pc:08x}'
        res += f' {instr:08x}'
        res += f' x{self.get_rd():02d}={rd:08x}'
        res += f' x{self.get_rs1():02d}={self._rs1_value:08x}'
        res += f' x{self.get_rs2():02d}={self._rs2_value:08x}'
        res += ' ' + self.mnem()
        return res

class Decoder:
    _register_bank: RegisterBank
    _memory: Memory

    def __init__(self, register_bank: RegisterBank, memory: Memory):
        self._register_bank = register_bank
        self._memory = memory

    def build_instruction(self, instruction: str) -> Instruction:
        opcode = slice_instruction(instruction, 0, 6)
        match opcode:
            case '1100011':
                return BTypeInstruction(instruction=instruction, register_bank=self._register_bank, memory=self._memory)
            case '0110111' | '0010111':
                return UTypeInstruction(instruction=instruction, register_bank=self._register_bank, memory=self._memory)
            case '1101111':
                return JTypeInstruction(instruction=instruction, register_bank=self._register_bank, memory=self._memory)
            case _:
                raise Exception(f'Unknown opcode in instruction: {instruction}')

class BTypeInstruction(Instruction):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def get_funct3(self):
        return slice_instruction(self._instr, 12, 14)

    def get_imm(self):
        res = 20 * slice_instruction(self._instr, 31, 31)
        res += slice_instruction(self._instr, 7, 7)
        res += slice_instruction(self._instr, 25, 30)
        res += slice_instruction(self._instr, 8, 11)
        res += '0'
        return res

    def name(self):
        match self.get_funct3():
            case '000':
                return 'beq'
            case '001':
                return 'bne'
            case '100':
                return 'blt'
            case '101':
                return 'bge'
            case '110':
                return 'bltu'
            case '111':
                return 'bgeu'
            case _:
                raise Exception(f'Unknown B-Type Instruction: {self._instr}')

    def exec(self):
        should_branch = False
        u_rs1 = to_uint(dec_to_twos_comp(self._rs1_value, 32))
        u_rs2 = to_uint(dec_to_twos_comp(self._rs2_value, 32))
        match self.name():
            case 'beq':
                should_branch = self._rs1_value == self._rs2_value
            case 'bne':
                should_branch = self._rs1_value != self._rs2_value
            case 'blt':
                should_branch = self._rs1_value < self._rs2_value
            case 'bge':
                should_branch = self._rs1_value >= self._rs2_value
            case 'bltu':
                should_branch = u_rs1 < u_rs2
            case 'bgeu':
                should_branch = u_rs1 >= u_rs2
        if should_branch:
            imm_ = twos_comp_to_dec(self.get_imm())
            self._register_bank.set_register('pc', self._pc + imm_)
        else:
            self._bump_pc()

    def mnem(self):
        rs1 = self._register_bank.get_alias(self.get_rs1())
        rs2 = self._register_bank.get_alias(self.get_rs2())
        imm = twos_comp_to_dec(self.get_imm())
        return f'{self.name()} {rs1}, {rs2}, {imm}'

class UTypeInstruction(Instruction):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def get_imm(self) -> str:
        return slice_instruction(self._instr, 12, 31) + 12 * '0'

    def name(self) -> str:
        opcode = slice_instruction(self._instr, 0, 6)
        match opcode:
            case '0110111':
                return 'lui'
            case '0010111':
                return 'auipc'
            case _:
                raise Exception(f'Unknown U-Type Instruction: {self._instr}')
    
    def exec(self):
        imm = twos_comp_to_dec(self.get_imm())
        match self.name():
            case 'lui':
                self._register_bank.set_register(self.get_rd(), imm)
            case 'auipc':
                self._register_bank.set_register(self.get_rd(), self._pc + imm)
        self._bump_pc()
    
    def mnem(self):
        imm = twos_comp_to_dec(self.get_imm()[:-12])
        rd = self._register_bank.get_alias(self.get_rd())
        return f'{self.name()} {rd}, {imm}'

class JTypeInstruction(Instruction):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def get_imm(self):
        res = 12 * slice_instruction(self._instr, 31, 31)
        res += slice_instruction(self._instr, 12, 19)
        res += slice_instruction(self._instr, 20, 20)
        res += slice_instruction(self._instr, 21, 30)
        res += '0'
        return res

    def name(self):
        return 'jal'

    def exec(self):
        imm = twos_comp_to_dec(self.get_imm())
        self._register_bank.set_register(self.get_rd(), self._pc + 4)
        self._register_bank.set_register('pc', self._pc + imm)
    
    def mnem(self):
        rd = self._register_bank.get_alias(self.get_rd())
        imm = twos_comp_to_dec(self.get_imm())
        return f'jal {rd}, {imm}'