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
_f:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	ldr	r2,	[fp, #8]			 @ charger variable e1
	push	{r2}		
	ldr	r2,	[fp, #4]			 @ charger variable e2
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	cmp	r0,	r1			 @ compare r0 et r1
	bgt	e0				 @ saut si > est vrai
	mov	r0,	#0			 @ résultat faux
	b	e1				 @ saut vers fin
e0:
	mov	r0,	#1			 @ résultat vrai
e1:
	push	{r0}				 @ empile le résultat
