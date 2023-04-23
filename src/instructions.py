import io

class InstructionsCache:
    _file: io.BufferedReader
    _instr_size: int

    def __init__(self, path: str, instr_size: int):
        self._file = open(path, 'rb')
        self._instr_size = instr_size

    def close(self):
        self._file.close()

    def load_instruction(self, address: int) -> int:
        self._file.seek(address, 0)
        instr = self._file.read(self._instr_size)
        return f'{int.from_bytes(instr, "little"):032b}'