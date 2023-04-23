class Memory:
    _memory: dict[int, str]
    _default: str

    def __init__(self, default: str = '00000000'):
        self._memory = {}
        self._default = default

    def load_byte(self, address: int) -> str:
        return self._memory.get(address, self._default)

    def save_byte(self, address: int, value: str) -> None:
        self._memory[address] = value

    # TODO: implementar helpers para acessar bytes específicos