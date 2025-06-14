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
_fibo:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	ldr	r2,	[fp, #4]			 @ charger variable n
	push	{r2}		
	mov	r1,	#1	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	cmp	r0,	r1			 @ compare r0 et r1
	ble	e2				 @ saut si <= est vrai
	mov	r0,	#0			 @ résultat faux
	b	e3				 @ saut vers fin
e2:
	mov	r0,	#1			 @ résultat vrai
e3:
	push	{r0}				 @ empile le résultat
	pop	{r1}				 @ dépile la condition
	cmp	r1,	#0			 @ teste si condition == 0 (faux)
	beq	e1				 @ saut si condition fausse
	mov	r1,	#1	
	push	{r1}		
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	b	e0				 @ saut vers la fin
e1:
e0:
	ldr	r2,	[fp, #4]			 @ charger variable n
	push	{r2}		
	mov	r1,	#1	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	sub	r0,	r0,	r1		 @ effectue la soustraction
	push	{r0}				 @ empile le résultat
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	ldr	r2,	[fp, #4]			 @ charger variable n
	push	{r2}		
	mov	r1,	#2	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	sub	r0,	r0,	r1		 @ effectue la soustraction
	push	{r0}				 @ empile le résultat
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	add	r0,	r0,	r1		 @ effectue l'addition
	push	{r0}				 @ empile le résultat
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut
	pop	{fp,pc}				 @ épilogue fonction
main:
	push	{fp,lr}		
	add	fp,	sp,	#4
	mov	r1,	#0	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#1	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#2	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#3	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#4	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#5	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#6	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#7	
	push	{r1}		
	bl	_fibo				 @ appel fonction fibo
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r0,	#0	
	pop	{fp, pc}		
