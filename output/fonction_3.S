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
_g:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	bl	_h				 @ appel fonction h
	push	{r2}				 @ empiler le résultat
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut
	pop	{fp,pc}				 @ épilogue fonction
_h:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	mov	r1,	#7	
	push	{r1}		
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut
	pop	{fp,pc}				 @ épilogue fonction
main:
	push	{fp,lr}		
	add	fp,	sp,	#4
	bl	_g				 @ appel fonction g
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r0,	#0	
	pop	{fp, pc}		
