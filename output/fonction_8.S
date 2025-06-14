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
_double:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	ldr	r2,	[fp, #4]			 @ charger variable e
	push	{r2}		
	ldr	r2,	[fp, #4]			 @ charger variable e
	push	{r2}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	add	r0,	r0,	r1		 @ effectue l'addition
	push	{r0}				 @ empile le résultat
	pop	{r0}				 @ valeur à affecter
	str	r0,	[fp, #4]			 @ affecter à e
	ldr	r2,	[fp, #4]			 @ charger variable e
	push	{r2}		
	pop	{r2}				 @ valeur de retour
	pop	{fp,pc}				 @ retour de fonction
	mov	r2,	#0			 @ retour par défaut
	pop	{fp,pc}				 @ épilogue fonction
_quadriple:
	push	{fp,lr}				 @ prologue fonction
	add	fp,	sp,	#4
	mov	r1,	#5	
	push	{r1}		
	bl	_double				 @ appel fonction double
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r0}				 @ ignorer le résultat
	ldr	r2,	[fp, #4]			 @ charger variable e
	push	{r2}		
	bl	_double				 @ appel fonction double
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	ldr	r2,	[fp, #4]			 @ charger variable e
	push	{r2}		
	bl	_double				 @ appel fonction double
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
	mov	r1,	#5	
	push	{r1}		
	bl	_double				 @ appel fonction double
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r0}				 @ ignorer le résultat
	mov	r1,	#10	
	push	{r1}		
	bl	_quadriple				 @ appel fonction quadriple
	add	sp,	sp,	#4		 @ dépiler les arguments
	push	{r2}				 @ empiler le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r0,	#0	
	pop	{fp, pc}		
