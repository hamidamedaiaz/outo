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
	pop	{r0}				 @ valeur pour variable a
	push	{r0}				 @ stocker variable a
	mov	r1,	#11	
	push	{r1}		
	pop	{r0}				 @ valeur pour variable b
	push	{r0}				 @ stocker variable b
e0:
	ldr	r2,	[fp, #-4]			 @ charger variable a
	push	{r2}		
	ldr	r2,	[fp, #-8]			 @ charger variable b
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	cmp	r0,	r1			 @ compare r0 et r1
	blt	e2				 @ saut si < est vrai
	mov	r0,	#0			 @ résultat faux
	b	e3				 @ saut vers fin
e2:
	mov	r0,	#1			 @ résultat vrai
e3:
	push	{r0}				 @ empile le résultat
	pop	{r1}				 @ dépile la condition
	cmp	r1,	#0			 @ teste si condition == 0 (faux)
	beq	e1				 @ saut si condition fausse
	mov	r1,	#2	
	push	{r1}		
	pop	{r0}				 @ valeur pour variable c
	push	{r0}				 @ stocker variable c
	ldr	r2,	[fp, #-4]			 @ charger variable a
	push	{r2}		
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	ldr	r2,	[fp, #-4]			 @ charger variable a
	push	{r2}		
	ldr	r2,	[fp, #-12]			 @ charger variable c
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	add	r0,	r0,	r1		 @ effectue l'addition
	push	{r0}				 @ empile le résultat
	pop	{r0}				 @ valeur à affecter
	str	r0,	[fp, #-4]			 @ affecter à a
	b	e0				 @ retour au début de la boucle
e1:
	mov	r1,	#12	
	push	{r1}		
	pop	{r0}				 @ valeur à affecter
	str	r0,	[fp, #-4]			 @ affecter à a
	mov	r1,	#64	
	push	{r1}		
	pop	{r0}				 @ valeur à affecter
	str	r0,	[fp, #-8]			 @ affecter à b
e4:
	ldr	r2,	[fp, #-4]			 @ charger variable a
	push	{r2}		
	ldr	r2,	[fp, #-8]			 @ charger variable b
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	cmp	r0,	r1			 @ compare r0 et r1
	blt	e6				 @ saut si < est vrai
	mov	r0,	#0			 @ résultat faux
	b	e7				 @ saut vers fin
e6:
	mov	r0,	#1			 @ résultat vrai
e7:
	push	{r0}				 @ empile le résultat
	pop	{r1}				 @ dépile la condition
	cmp	r1,	#0			 @ teste si condition == 0 (faux)
	beq	e5				 @ saut si condition fausse
	mov	r1,	#5	
	push	{r1}		
	pop	{r0}				 @ valeur pour variable c
	push	{r0}				 @ stocker variable c
	ldr	r2,	[fp, #-4]			 @ charger variable a
	push	{r2}		
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	ldr	r2,	[fp, #-4]			 @ charger variable a
	push	{r2}		
	ldr	r2,	[fp, #-16]			 @ charger variable c
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	add	r0,	r0,	r1		 @ effectue l'addition
	push	{r0}				 @ empile le résultat
	pop	{r0}				 @ valeur à affecter
	str	r0,	[fp, #-4]			 @ affecter à a
	b	e4				 @ retour au début de la boucle
e5:
	mov	r0,	#0	
	pop	{fp, pc}		
