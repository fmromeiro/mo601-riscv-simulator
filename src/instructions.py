import io
from memory import Memory
from utils import dec_to_twos_comp

class InstructionsCache:
    _memory: Memory
    _instr_size: int

    def __init__(self, path: str, instr_size: int, memory: Memory, offset: int):
        self._instr_size = instr_size
        self._memory = memory
        self._fill_memory(path, offset)

    def _fill_memory(self, path, offset):
        i = offset
        with open(path, 'rb') as f:
            while True:
                value = f.read(1)
                if value == b'': break
                value = dec_to_twos_comp(int.from_bytes(value, 'little'), 8)
                self._memory.save_byte(i, value)
                i += 1

    def close(self):
        self._file.close()

    def load_instruction(self, address: int) -> int:
        return ''.join(
            reversed([self._memory.load_byte(address + i) for i in range(4)]))