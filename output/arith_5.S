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
	mov	r1,	#23	
	push	{r1}		
	mov	r1,	#10	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	mov	r2,	r0			 @ copie r0 dans r2
	mul	r0,	r1,	r2		 @ r0 = r1 * r2
	push	{r0}				 @ empile le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#0	
	push	{r1}		
	mov	r1,	#23	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	sub	r0,	r0,	r1		 @ effectue la soustraction
	push	{r0}				 @ empile le résultat
	mov	r1,	#10	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	mov	r2,	r0			 @ copie r0 dans r2
	mul	r0,	r1,	r2		 @ r0 = r1 * r2
	push	{r0}				 @ empile le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#23	
	push	{r1}		
	mov	r1,	#0	
	push	{r1}		
	mov	r1,	#10	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	sub	r0,	r0,	r1		 @ effectue la soustraction
	push	{r0}				 @ empile le résultat
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	mov	r2,	r0			 @ copie r0 dans r2
	mul	r0,	r1,	r2		 @ r0 = r1 * r2
	push	{r0}				 @ empile le résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#0	
	push	{r1}		
	mov	r1,	#23	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	sub	r0,	r0,	r1		 @ effectue la soustraction
	push	{r0}				 @ empile le résultat
	mov	r1,	#0	
	push	{r1}		
	mov	r1,	#10	
	push	{r1}		
	pop	{r1}				 @ dépile exp2 dans r1
	pop	{r0}				 @ dépile exp1 dans r0
	sub	r0,	r0,	r1		 @ effectue la soustraction
	push	{r0}				 @ empile le résultat
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
