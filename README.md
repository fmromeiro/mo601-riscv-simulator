# mo601-riscv-simulator
 Implementação de um simulador de RISC-V para a matéria MO601 da Unicamp 

## Introdução

Nesse projeto implementamos um simulador de RISC-V 32IM em Python 3.10. Ele lê os binários extraídos dos ELFs resultantes da compilação de código C para RISC-V e gera arquivos de log listando os valores dos registradores e o disassembly para cada instrução.

## Execução

O simulador foi programado e testado com Python 3.10.10. O script de preparação dos testes depende do comando `riscv64-linux-gnu-objcopy`.

Para executar o projeto, primeiro transformamos os arquivos ELF compilados para arquivos binários que o simulador consegue interpretar. Para isso, executamos o comando a seguir, substituindo `[dir]` pela pasta onde os arquivos ELF (de extensão .riscv) estão localizados.

> `./build.sh [dir]`

Esse comando vai colocar os binários extraídos dos ELFs no caminho `test/build/bin`.

Depois de rodar o script, podemos executar o simulador com o comando a seguir

> `python src/main.py`

O simulador irá buscar pelos binários na pasta `test/build/bin` e irá colocar os arquivos de saída com a extensão `.log` na pasta `test/`.