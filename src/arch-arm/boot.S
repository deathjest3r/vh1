

.global _start
_start:
	//ldr r0, =vh1
	//bl .printh

	/* Setting SCTLR
	 * Setting Bit 13 = Vectors High and
	 * and Bit 2 = Disable all caches
	 */
	//ldr r0, =sctlr
	//bl .printh
	//mov r0, #(1 <<1)
	//add r0, r0, #(1<<12)
	//mcr p15, 0, r0, c1, c0, 0

	mov r1, #0x10000000
	add r1, r1, #0x9000
	mov r2, #'V'
	str r2, [r1]

	//ldr r0, =ttbcr
	//bl .printh
	mov r0, #0x20
	mcr p15, 0, r0, c2, c0, 2

	mov	r4, #0x01
	mcr	p15, #0, r4, c3, c0, 0		// DACR
	orr	r4, r4, r4, lsl #16
	mcr	p15, #0, r4, c10, c2, 1		// NMRR
	mov	r4, #0x02
	mcr	p15, #0, r4, c10, c2, 0		// PRRR

	// Enable paging
	//ldr r0, =page
	//bl .printh
	mov r0, #0x68000000
	orr r0, r0, #2
	mcr	p15, #0, r0, c2, c0, 0

	mrc	p15, #0, r4, c1, c0, 0
	orr	r4, r4, #0x10000005
	bic	r4, r4, #0x02
	mcr	p15, #0, r4, c1, c0, 0		// SCTLR: set {TRE, C, M}, clear {A}
	isb
	dsb	sy

	//mov r1, #0x10000000
	//add r1, r1, #0x9000
	mov r1, # 0xf7000000
	mov r2, #'V'
	str r2, [r1]

	/* Finnaly jumping to C code */
	//b main

/*
 * Simple print function for early output
 * Input: r0 = String to print
 * Output: -
 */
.printh:
	mov r1, #0x10000000
	add r1, r1, #0x9000
	mov r3, #'\n'
.1: ldrb r2, [r0]
	str r2, [r1]
	add r0, r0, #1
	cmp r3, r0
	#bne .1
	bx lr

vh1:	.ascii "Starting VH1\r\n============\n"
sctlr:	.ascii "* Setting SCTLR\n"
page:	.ascii "* Enabling Paging\n"
ttbcr:	.ascii "* Setting TTBCR\n"
