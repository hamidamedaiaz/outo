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
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut (Faux)
	pop	{fp,pc}				 @ épilogue fonction
_g:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	ldr	r2,	[fp, #8]			 @ charger variable b1
	push	{r2}		
	pop	{r1}				 @ dépile la condition
	cmp	r1,	#0			 @ teste si condition == 0 (faux)
	beq	e3				 @ saut si condition fausse
	ldr	r2,	[fp, #4]			 @ charger variable e2
	push	{r2}		
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	b	e2				 @ saut vers la fin
e3:
e2:
	mov	r1,	#0	
	push	{r1}		
	ldr	r2,	[fp, #4]			 @ charger variable e2
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	sub	r0,	r0,	r1		 @ effectue la soustraction
	push	{r0}				 @ empile le résultat
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut
	pop	{fp,pc}				 @ épilogue fonction
_h:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	ldr	r2,	[fp, #12]			 @ charger variable e1
	push	{r2}		
	ldr	r2,	[fp, #8]			 @ charger variable e2
	push	{r2}		
	ldr	r2,	[fp, #4]			 @ charger variable e3
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	mov	r2,	r0			 @ copie r0 dans r2
	mul	r0,	r1,	r2		 @ r0 = r1 * r2
	push	{r0}				 @ empile le résultat
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
	mov	r1,	#2	
	push	{r1}		
	mov	r1,	#1	
	push	{r1}		
	bl	_f				 @ appel fonction f
	add	sp,	sp,	#8		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#4	
	push	{r1}		
	mov	r1,	#0	
	push	{r1}		
	bl	_g				 @ appel fonction g
	add	sp,	sp,	#8		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#5	
	push	{r1}		
	mov	r1,	#1	
	push	{r1}		
	bl	_g				 @ appel fonction g
	add	sp,	sp,	#8		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#3	
	push	{r1}		
	mov	r1,	#2	
	push	{r1}		
	mov	r1,	#1	
	push	{r1}		
	bl	_h				 @ appel fonction h
	add	sp,	sp,	#12		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r0,	#0	
	pop	{fp, pc}		
