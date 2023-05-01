from utils import *

def get_name(opcode, funct3, funct7, _instr):
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
                    raise Exception(f'Unknown R-Type Instruction: {_instr}')
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
                    raise Exception(f'Unknown R-Type Instruction: {_instr}')


def add(rs1, rs2, imm):
    return rs1 + rs2

def sub(rs1, rs2, imm):
    return rs1 - rs2

def sll(rs1, rs2, imm):
    return rs1 << rs2

def srl(rs1, rs2, imm):
    b_rs1 = dec_to_twos_comp(rs1, 32)
    srl_rs1 = '0' * rs2 + b_rs1[:32-rs2]
    return twos_comp_to_dec(srl_rs1)

def sra(rs1, rs2, imm):
    b_rs1 = dec_to_twos_comp(rs1, 32)
    # print(rs1, rs2, b_rs1)
    sra_rs1 = extend_signal(b_rs1[:32-rs2], 32)
    return twos_comp_to_dec(sra_rs1)

def slt(rs1, rs2, imm):
    return 1 if rs1 < rs2 else 0

def sltu(rs1, rs2, imm):
    u_rs1 = to_uint(dec_to_twos_comp(rs1, 32))
    u_rs2 = to_uint(dec_to_twos_comp(rs2, 32))
    return int(u_rs1 < u_rs2)

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
    if rs1 == -(2**31) and rs2 == -1:
        return rs1
    if rs2 == 0:
        return -1
    if rs1 < 0:
        if rs2 < 0:
            return (-rs1)//(-rs2)
        return -((-rs1)//rs2)
    if rs2 < 0:
        return -(rs1//(-rs2))
    return rs1 // rs2

def divu(rs1, rs2, imm):
    return int_to_uint(rs1) // int_to_uint(rs2)

def rem(rs1, rs2, imm):
    if rs1 == -(2**31) and rs2 == -1:
        return 0
    if rs2 == 0:
        return rs1
    if rs1 < 0:
        if rs2 < 0:
            return (-rs1)%(-rs2)
        return -((-rs1)%rs2)
    if rs2 < 0:
        return -(rs1%(-rs2))
    return rs1 % rs2

def remu(rs1, rs2, imm):
    if rs2 == 0:
        return 2**32 - 1
    return int_to_uint(rs1) % int_to_uint(rs2)

__fundict = {
    'remu': remu,
    'rem': rem,
    'divu': divu,
    'div': div,
    'mulhsu': mulhsu,
    'mulh': mulh,
    'mulhu': mulhu,
    'mul': mul,
    'and': and_,
    'or': or_,
    'xor': xor,
    'sltu': sltu,
    'slt': slt,
    'sll': sll,
    'srl': srl,
    'sra': sra,
    'sub': sub,
    'add': add,
}

def exec(name, rs1, rs2, imm):
    return __fundict[name](rs1, rs2, imm)
