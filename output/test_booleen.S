.LC0:
    .ascii	"%d\000"
    .align	2
.LC1:
    .ascii	"%d\012\000"
    .text
    .align	2
    .global	main
    .global __aeabi_idiv
    .global __aeabi_idivmod
main:
	push	{fp,lr}		
	add	fp,	sp,	#4
	mov	r1,	#1	
	push	{r1}		
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
