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
