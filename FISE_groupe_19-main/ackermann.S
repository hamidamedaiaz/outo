.LC0:
    .ascii "%d\000"
    .align 2
.LC1:
    .ascii "%d\012\000"
    .text
    .align 2
    .global main
    .global __aeabi_idiv
    .global __aeabi_idivmod
_ack:
	push	{fp,lr}		
	mov	fp,	sp	
	sub	sp,	sp,	#8
	str	r0,	[fp,#-4]	
	str	r1,	[fp,#-8]	
	ldr	r2,	[fp,#-4]	
	push	{r2}		
	mov	r1,	#0	
	push	{r1}		
	pop	{r1}		
	pop	{r0}		
	cmp	r0,	r1	
	beq	e2		
	mov	r0,	#0	
	b	e3		
e2:
	mov	r0,	#1	
e3:
	push	{r0}		
	pop	{r1}		
	cmp	r1,	#0	
	beq	e1		
	ldr	r2,	[fp,#-8]	
	push	{r2}		
	mov	r1,	#1	
	push	{r1}		
	pop	{r1}		
	pop	{r0}		
	add	r0,	r0,	r1
	push	{r0}		
	pop	{r0}		
	b	ack_end		
	b	e0		
e1:
	ldr	r2,	[fp,#-8]	
	push	{r2}		
	mov	r1,	#0	
	push	{r1}		
	pop	{r1}		
	pop	{r0}		
	cmp	r0,	r1	
	beq	e5		
	mov	r0,	#0	
	b	e6		
e5:
	mov	r0,	#1	
e6:
	push	{r0}		
	pop	{r1}		
	cmp	r1,	#0	
	beq	e4		
	ldr	r2,	[fp,#-4]	
	push	{r2}		
	mov	r1,	#1	
	push	{r1}		
	pop	{r1}		
	pop	{r0}		
	sub	r0,	r0,	r1
	push	{r0}		
	mov	r1,	#1			 @ chargement littéral
	push	{r1}		
	pop	{r1}				 @ charger argument 1
	pop	{r0}				 @ charger argument 0
	bl	_ack				 @ appel ack
	push	{r0}				 @ empiler résultat
	pop	{r0}		
	b	ack_end		
	b	e0		
e4:
	ldr	r2,	[fp,#-4]	
	push	{r2}		
	mov	r1,	#1	
	push	{r1}		
	pop	{r1}		
	pop	{r0}		
	sub	r0,	r0,	r1
	push	{r0}		
	ldr	r2,	[fp,#-4]	
	push	{r2}		
	ldr	r2,	[fp,#-8]	
	push	{r2}		
	mov	r1,	#1	
	push	{r1}		
	pop	{r1}		
	pop	{r0}		
	sub	r0,	r0,	r1
	push	{r0}		
	pop	{r1}				 @ charger argument 1
	pop	{r0}				 @ charger argument 0
	bl	_ack				 @ appel ack
	push	{r0}				 @ empiler résultat
	pop	{r1}				 @ charger argument 1
	pop	{r0}				 @ charger argument 0
	bl	_ack				 @ appel ack
	push	{r0}				 @ empiler résultat
	pop	{r0}		
	b	ack_end		
e0:
	b	ack_end		
ack_end:
	add	sp,	sp,	#8
	pop	{fp,pc}		
main:
	push	{fp,lr}		
	mov	fp,	sp	
	mov	r1,	#1			 @ chargement littéral
	push	{r1}		
	mov	r1,	#2			 @ chargement littéral
	push	{r1}		
	pop	{r1}				 @ charger argument 1
	pop	{r0}				 @ charger argument 0
	bl	_ack				 @ appel ack
	push	{r0}				 @ empiler résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#2			 @ chargement littéral
	push	{r1}		
	mov	r1,	#2			 @ chargement littéral
	push	{r1}		
	pop	{r1}				 @ charger argument 1
	pop	{r0}				 @ charger argument 0
	bl	_ack				 @ appel ack
	push	{r0}				 @ empiler résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#3			 @ chargement littéral
	push	{r1}		
	mov	r1,	#1			 @ chargement littéral
	push	{r1}		
	pop	{r1}				 @ charger argument 1
	pop	{r0}				 @ charger argument 0
	bl	_ack				 @ appel ack
	push	{r0}				 @ empiler résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r1,	#3			 @ chargement littéral
	push	{r1}		
	mov	r1,	#2			 @ chargement littéral
	push	{r1}		
	pop	{r1}				 @ charger argument 1
	pop	{r0}				 @ charger argument 0
	bl	_ack				 @ appel ack
	push	{r0}				 @ empiler résultat
	pop	{r1}		
	ldr	r0,	=.LC1	
	bl	printf		
	mov	r0,	#0	
	pop	{fp, pc}		
