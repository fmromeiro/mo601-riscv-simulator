REGISTER_ALIASES = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0',
                    's1', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 's2',
                    's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11',
                    't3', 't4', 't5', 't6']

class RegisterBank:
    _bank: dict
    _default: int

    def __init__(self, default: int = 0):
        self._bank = {}
        self._default = default

    def set_register(self, name, value: int) -> None:
        if name != 0:
            self._bank[name] = value

    def get_register(self, name) -> int:
        return self._bank.get(name, self._default)

    def get_alias(self, idx: int) -> str:
        return REGISTER_ALIASES[idx]