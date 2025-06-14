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
	mov	r1,	#2	
	push	{r1}		
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut
	pop	{fp,pc}				 @ épilogue fonction
_g:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	mov	r1,	#4	
	push	{r1}		
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut
	pop	{fp,pc}				 @ épilogue fonction
_h:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	mov	r1,	#1	
	push	{r1}		
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut (Faux)
	pop	{fp,pc}				 @ épilogue fonction
main:
	push	{fp,lr}		
	add	fp,	sp,	#4
	bl	_f				 @ appel fonction f
	push	{r2}				 @ empiler le résultat
	bl	_g				 @ appel fonction g
	push	{r2}				 @ empiler le résultat
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	add	r0,	r0,	r1		 @ effectue l'addition
	push	{r0}				 @ empile le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	bl	_h				 @ appel fonction h
	push	{r2}				 @ empiler le résultat
	pop	{r0}				 @ dépile exp1 dans r0
	cmp	r0,	#0			 @ compare à 0
	moveq	r0,	#1			 @ si égal à 0 -> 1
	movne	r0,	#0			 @ sinon -> 0
	push	{r0}				 @ empile le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r0,	#0	
	pop	{fp, pc}		
