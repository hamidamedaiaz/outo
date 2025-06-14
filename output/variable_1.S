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
	mov	r1,	#4	
	push	{r1}		
	pop	{r0}				 @ valeur pour variable a
	push	{r0}				 @ stocker variable a
	mov	r1,	#3	
	push	{r1}		
	pop	{r0}				 @ valeur pour variable b
	push	{r0}				 @ stocker variable b
	ldr	r2,	[fp, #-4]			 @ charger variable a
	push	{r2}		
	ldr	r2,	[fp, #-8]			 @ charger variable b
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	mov	r2,	r0			 @ copie r0 dans r2
	mul	r0,	r1,	r2		 @ r0 = r1 * r2
	push	{r0}				 @ empile le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r0,	#0	
	pop	{fp, pc}		
