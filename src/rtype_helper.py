from utils import *

def get_name(opcode, funct3, funct7, _instr):
    if opcode == '0010011':
            match funct3:
                case '000':
                    return 'addi'
                case '001':
                    return 'slli'
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
                case '101':
                    match funct7:
                        case '0000000':
                            return 'srli'
                        case '0100000':
                            return 'srai'
        elif opcode == '0110011':
            if funct7 == '0000001':
                match funct3:
                    case '000':
                        return 'mul'
                    case '001':
                        return 'mulh'
                    case '010':
                        return 'mulhsu'
                    case '011':
                        return 'mulhu'
                    case '100':
                        return 'div'
                    case '101':
                        return 'divu'
                    case '110':
                        return 'rem'
                    case '111':
                        return 'remu'
            match funct3:
                case '000':
                    match funct7:
                        case '0000000':
                            return 'add'
                        case '0100000':
                            return 'sub'
                        case _:
                            raise Exception(f'Unknown S-Type Instruction: {_instr}')
                case '001':
                    return 'sll'
                case '010':
                    return 'slt'
                case '011':
                    return 'sltu'
                case '100':
                    return 'xor'
                case '110':
                    return 'or'
                case '111':
                    return 'and'
                case '101':
                    match funct7:
                        case '0000000':
                            return 'srl'
                        case '0100000':
                            return 'sra'
                        case _:
                            raise Exception(f'Unknown S-Type Instruction: {_instr}')



def addi(rs1, rs2, imm):
    return rs1 + twos_comp_to_dec(imm)

def slli(rs1, rs2, imm):
    return rs1 << twos_comp_to_dec(imm)

def slti(rs1, rs2, imm):
    return 1 if rs1 < twos_comp_to_dec(imm) else 0

def sltiu(rs1, rs2, imm):
    return 1 if int_to_uint(rs1) < to_uint(imm) else 0

def xori(rs1, rs2, imm):
    return rs1 ^ to_uint(imm)

def ori(rs1, rs2, imm):
    return rs1 | to_uint(imm)

def andi(rs1, rs2, imm):
    return rs1 & to_uint(imm)

def add(rs1, rs2, imm):
    return rs1 + rs2

def sub(rs1, rs2, imm):
    return rs1 - rs2

def sll(rs1, rs2, imm):
    return rs1 << rs2

def slt(rs1, rs2, imm):
    return 1 if rs1 < rs2 else 0

def sltu(rs1, rs2, imm):
    return 1 if int_to_uint(rs1) < to_uint(imm) else 0

def xor(rs1, rs2, imm):
    return rs1 ^ rs2

def or_(rs1, rs2, imm):
    return rs1 | rs2

def and_(rs1, rs2, imm):
    return rs1 & rs2

def mul(rs1, rs2, imm):
    return (rs1 * rs2) & 0b11111111111111111111111111111111

def mulh(rs1, rs2, imm):
    return (rs1 * rs2) & 0b1111111111111111111111111111111100000000000000000000000000000000

def mulhu(rs1, rs2, imm):
    return (int_to_uint(rs1) * int_to_uint(rs2)) & 0b1111111111111111111111111111111100000000000000000000000000000000

def mulhsu(rs1, rs2, imm):
    return (rs1 * int_to_uint(rs2)) & 0b1111111111111111111111111111111100000000000000000000000000000000

def div(rs1, rs2, imm):
    return rs1 // rs2

def divu(rs1, rs2, imm):
    return int_to_uint(rs1) // int_to_uint(rs2)

def rem(rs1, rs2, imm):
    return rs1 % rs2

def remu(rs1, rs2, imm):
    return int_to_uint(rs1) % int_to_uint(rs2)

__fundict = {
    'remu': remu,
    'rem': rem,
    'divu': divu,
    'div': div,
    'mulhsu': mulhsu,
    'mulh': mulh,
    'mul': mul,
    'and': and_,
    'or': or_,
    'xor': xor,
    'sltu': sltu,
    'slt': slt,
    'sll': sll,
    'sub': sub,
    'add': add,
    'andi': andi,
    'ori': ori,
    'xori': xori,
    'sltiu': sltiu,
    'slti': slti,
    'slli': slli,
    'addi': addi,
}

def exec(name, rs1, rs2, imm):
    return __fundict[name](rs1, rs2, imm)
