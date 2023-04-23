WORD_SIZE = 32
BYTES_IN_WORD = 4

def slice_instruction(instr: str, lo: int, hi: int) -> str:
    return instr[WORD_SIZE - 1 - hi : WORD_SIZE - lo]

def to_uint(bits: str) -> int:
    return int(bits, base=2)

def twos_comp_to_dec(val: str) -> int:
    if val[0] == '0':
        return int(val, 2)
    inverted = (1 - int(x) for x in reversed(val))
    abs_ = 0
    c = 1
    for i, x in enumerate(inverted):
        abs_ += ((x + c) % 2) * 2 ** i
        c = (x + c) // 2
    return -abs_

def _pos_dec_to_twos_comp(val: int, size: int) -> str:
    res = f'{val:b}'
    if len(res) >= size:
        return res[:size]
    return ((size - len(res)) * '0') + res

def dec_to_twos_comp(val: int, size: int) -> str:
    if val > 0:
        return _pos_dec_to_twos_comp(val, size)
    val *= -1
    aux = _pos_dec_to_twos_comp(val, size)
    aux = (1 - int(x) for x in reversed(aux))
    res = ''
    c = 1
    for i in aux:
        res = str((i + c) % 2) + res
        c = (i + c) // 2
    return res