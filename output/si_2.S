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
	pop	{r0}				 @ dépile exp1 dans r0
	cmp	r0,	#0			 @ compare à 0
	moveq	r0,	#1			 @ si égal à 0 -> 1
	movne	r0,	#0			 @ sinon -> 0
	push	{r0}				 @ empile le résultat
	pop	{r1}				 @ dépile la condition
	cmp	r1,	#0			 @ teste si condition == 0 (faux)
	beq	e1				 @ saut si condition fausse
	mov	r1,	#3	
	push	{r1}		
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	b	e0				 @ saut vers la fin
e1:
e0:
	mov	r1,	#0	
	push	{r1}		
	pop	{r0}				 @ dépile exp1 dans r0
	cmp	r0,	#0			 @ compare à 0
	moveq	r0,	#1			 @ si égal à 0 -> 1
	movne	r0,	#0			 @ sinon -> 0
	push	{r0}				 @ empile le résultat
	pop	{r1}				 @ dépile la condition
	cmp	r1,	#0			 @ teste si condition == 0 (faux)
	beq	e3				 @ saut si condition fausse
	mov	r1,	#4	
	push	{r1}		
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	b	e2				 @ saut vers la fin
e3:
e2:
	mov	r0,	#0	
	pop	{fp, pc}		
