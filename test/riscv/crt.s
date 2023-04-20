/*************************************************
**************************************************
*	@file		crt.S
*	@author		Dário Dias
*	@email		dsd@cin.ufpe.br		
*	@version	0.20
*	@date		9 July 2016
*	@brief		The ArchC Risc-V functional model.
**************************************************
*************************************************/

#include "encoding.h"

#define STACK_SIZE 524288

  .text
  .globl _start
  .equ memory_size, 0x20000000

_start:
  lui sp,0x500
  jal main
  lui t0, 0x20000
  jalr t0, 0x0
  ebreak

.bss
.align 8
.skip 4096
kstacktop:

.section .tbss
tls_start:
