from register import RegisterBank
from memory import Memory
from instructions import InstructionsCache
from utils import *

import rtype_helper


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
        vals = {'rd':rd, 'rs1': self._rs1_value, 'rs2': self._rs2_value}
        for val in vals:
            vals[val] = to_uint(dec_to_twos_comp(vals[val], 32))
        instr = int(self._instr, 2)
        res = f'PC={self._pc:08x}'
        res += f' [{instr:08x}]'
        res += f' x{self.get_rd():02d}={vals["rd"]:08x}'
        res += f' x{self.get_rs1():02d}={vals["rs1"]:08x}'
        res += f' x{self.get_rs2():02d}={vals["rs2"]:08x}'
        res += f' {self.name():<8}' + self.mnem()
        return res

    def is_end(self):
        return False

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
            case '0100011':
                return STypeInstruction(instruction=instruction, register_bank=self._register_bank, memory=self._memory)
            case '0000011' | '0010011' | '1100111' :
                return ITypeInstruction(instruction=instruction, register_bank=self._register_bank, memory=self._memory)
            case '0110011':
                return RTypeInstruction(instruction=instruction, register_bank=self._register_bank, memory=self._memory)
            case '1110011':
                return EBreakInstruction(instruction=instruction, register_bank=self._register_bank, memory=self._memory)
            case _:
                raise Exception(f'Unknown opcode in instruction: {instruction}')

class EBreakInstruction(Instruction):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def exec(self):
        return

    def name(self):
        return 'ebreak'

    def mnem(self):
        return ''

    def is_end(self):
        return True

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
        return f'{rs1}, {rs2}, 0x{self._pc + imm:x}'

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
        return f'{rd}, {imm}'

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
        return f'jal {rd}, 0x{self._pc + imm:x}'
    
class STypeInstruction(Instruction):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def get_imm(self):
        res = slice_instruction(self._instr, 25, 31)
        res += slice_instruction(self._instr, 7, 11)
        return res

    def get_funct3(self):
        return slice_instruction(self._instr, 12, 14)

    def name(self) -> str:
        match self.get_funct3():
            case '000':
                return 'sb'
            case '001':
                return 'sh'
            case '010':
                return 'sw'
            case _:
                raise Exception(f'Unknown S-Type Instruction: {self._instr}')

    def exec(self):
        imm = twos_comp_to_dec(self.get_imm())
        rs1 = self._register_bank.get_register(self.get_rs1())
        rs2 = self._register_bank.get_register(self.get_rs2())

        width = 2 ** int(self.get_funct3(), base=2)
        value = dec_to_twos_comp(rs2, 32)

        for i in range(width):
            value_slice = slice_instruction(value, i*8, i*8 + 7)
            # print(self.name(), rs1 + imm + width - i - 1, i, value, value_slice)
            self._memory.save_byte(rs1 + imm + width - i - 1, value_slice)
        self._bump_pc()
    
    def mnem(self):
        imm = twos_comp_to_dec(self.get_imm())
        rs1 = self._register_bank.get_alias(self.get_rs1())
        rs2 = self._register_bank.get_alias(self.get_rs2())
        return f'{rs2}, {imm}({rs1})'

class ITypeInstruction(Instruction):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def get_imm(self):
        res = slice_instruction(self._instr, 20, 31)
        return res

    def get_funct3(self):
        return slice_instruction(self._instr, 12, 14)
    
    def name(self) -> str:
        opcode = slice_instruction(self._instr, 0, 6)
        upper_imm = self.get_imm()[:7]
        if opcode == '1100111':
            return 'jalr'
        elif opcode == '0000011':
            match self.get_funct3():
                case '000':
                    return 'lb'
                case '001':
                    return 'lh'
                case '010':
                    return 'lw'
                case '100':
                    return 'lbu'
                case '101':
                    return 'lhu'
                case _:
                    raise Exception(f'Unknown S-Type Instruction: {self._instr}')
        elif opcode == '0010011':
            match self.get_funct3():
                case '000':
                    return 'addi'
                case '010':
                    return 'slti'
                case '011':
                    return 'sltiu'
                case '100':
                    return 'xori'
                case '110':
                    return 'ori'
                case '111':
                    return 'andi'
                case '001':
                    return 'slli'
                case '101':
                    if upper_imm == '0000000':
                        return 'srli'
                    elif upper_imm == '0100000':
                        return 'srai'
                    else:
                        raise Exception(f'Unknown S-Type Instruction: {self._instr}')
                case _:
                    raise Exception(f'Unknown S-Type Instruction: {self._instr}')
        else:
            raise Exception(f'Unknown S-Type Instruction: {self._instr}')

    def exec(self):
        imm = twos_comp_to_dec(self.get_imm())
        rs1 = self._register_bank.get_register(self.get_rs1())

        if self.name() == 'jalr':
            dest = dec_to_twos_comp(rs1 + imm, 32)
            dest = dest[:-1] + '0'
            dest = twos_comp_to_dec(dest)
            self._register_bank.set_register(self.get_rd(), self._pc + 4)
            self._register_bank.set_register('pc', dest)
            return

        self._bump_pc()
        if self.name()[0] == 'l':
            width = 2 ** int(slice_instruction(self._instr, 12, 13), base=2)
            value = ''

            for i in range(width):
                a = self._memory.load_byte(rs1 + imm + i)
                value += self._memory.load_byte(rs1 + imm + i)
                # print(self.name(), value, a, width, i, rs1 + imm + i)

            if slice_instruction(self._instr, 14, 14) == '1': # unsigned
                self._register_bank.set_register(self.get_rd(), to_uint(value))
            else:
                self._register_bank.set_register(self.get_rd(), twos_comp_to_dec(value))
            return

        b_rs1 = dec_to_twos_comp(self._rs1_value, 32)
        u_rs1 = to_uint(b_rs1)
        b_imm = extend_signal(self.get_imm(), 32)
        u_imm = to_uint(b_imm)
        shamt = to_uint(self.get_imm()[-5:])
        val = None
        match self.name():
            case 'addi':
                val = self._rs1_value + imm
            case 'slti':
                val = 1 if self._rs1_value < imm else 0
            case 'sltiu':
                val = 1 if u_rs1 < u_imm else 0
            case 'xori':
                val = twos_comp_to_dec(''.join(str(int(x != y)) for x, y in zip(b_imm, b_rs1)))
            case 'ori':
                val = twos_comp_to_dec(''.join(str(int('1' in (x, y))) for x, y in zip(b_imm, b_rs1)))
            case 'andi':
                val = twos_comp_to_dec(''.join(str(int(x == y == '1')) for x, y in zip(b_imm, b_rs1)))
            case 'slli':
                val = twos_comp_to_dec((b_rs1 + shamt * '0')[-32:])
                # if self._pc == 0x164:
                #     print(self._rs1_value, b_rs1, self.get_imm(), shamt, val)
                #     input()
            case 'srli':
                val = twos_comp_to_dec((shamt * '0' + b_rs1)[:32])
            case 'srai':
                val = twos_comp_to_dec((shamt * b_rs1[0] + b_rs1)[:32])
        self._register_bank.set_register(self.get_rd(), val)

    def mnem(self):
        rs1 = self._register_bank.get_alias(self.get_rs1())
        rd = self._register_bank.get_alias(self.get_rd())
        imm = twos_comp_to_dec(self.get_imm())
        pc = self._register_bank.get_register('pc')
        name = self.name()
        if name == 'jalr':
            return f'{rd}, {rs1}, 0x{pc:x}'
        elif name[0] == 'l':
            return f'{rd}, {imm}({rs1})'
        return f'{rd}, {rs1}, {imm}'

class RTypeInstruction(Instruction):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def get_imm(self):
        return slice_instruction(self._instr, 20, 31)

    def get_funct3(self):
        return slice_instruction(self._instr, 12, 14)

    def get_funct7(self):
        return slice_instruction(self._instr, 25, 31)
    
    def name(self) -> str:
        opcode = slice_instruction(self._instr, 0, 6)
        funct3 = self.get_funct3()
        funct7 = self.get_funct7()
        return rtype_helper.get_name(opcode, funct3, funct7, self._instr)

    def exec(self):
        imm = self.get_imm()
        rs1 = self._register_bank.get_register(self.get_rs1())
        rs2 = self._register_bank.get_register(self.get_rs2())
        name = self.name()
        # print(self._memory._memory)
        # print(self._instr)

        value = rtype_helper.exec(name, rs1, rs2, imm)

        self._register_bank.set_register(self.get_rd(), value)
        self._bump_pc()

    def mnem(self):
        opcode = slice_instruction(self._instr, 0, 6)
        rs1 = self._register_bank.get_alias(self.get_rs1())
        rd = self._register_bank.get_alias(self.get_rd())
        if opcode == '0010011':
            imm = twos_comp_to_dec(self.get_imm())
            return f'{rd}, {rs1}, {imm}'
        rs2 = self._register_bank.get_alias(self.get_rs2())
        return f'{rd}, {rs1}, {rs2}'