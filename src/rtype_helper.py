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
    return rs1 + imm

def slli(rs1, rs2, imm):
    pass

def slti(rs1, rs2, imm):
    pass

def sltiu(rs1, rs2, imm):
    pass

def xori(rs1, rs2, imm):
    pass

def ori(rs1, rs2, imm):
    pass

def andi(rs1, rs2, imm):
    pass

def add(rs1, rs2, imm):
    pass

def sub(rs1, rs2, imm):
    pass

def sll(rs1, rs2, imm):
    pass

def sltv(rs1, rs2, imm):
    pass

def sltu(rs1, rs2, imm):
    pass

def xor(rs1, rs2, imm):
    pass

def or_(rs1, rs2, imm):
    pass

def and_(rs1, rs2, imm):
    pass

def mul(rs1, rs2, imm):
    pass

def mulh(rs1, rs2, imm):
    pass

def mulhsu(rs1, rs2, imm):
    pass

def div(rs1, rs2, imm):
    pass

def divu(rs1, rs2, imm):
    pass

def rem(rs1, rs2, imm):
    pass

def remu(rs1, rs2, imm):
    pass

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
    'sltv': sltv,
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