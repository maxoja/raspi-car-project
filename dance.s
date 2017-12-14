.data

.balign 4
interval: .int 250

.balign 4
pin_left_a: .int 2
.balign 4
pin_left_b: .int 3
.balign 4
pin_right_a: .int 7
.balign 4
pin_right_b: .int 0

.text
.global main

.extern wiringPiSetup
.extern delay
.extern digitalWrite
.extern pinMode

main:
	push {lr}	
	
_setup_wiringPi:

	bl wiringPiSetup	/*	return result at r0	*/
	cmp R0, #-1
	bne _run		/*	not error -> run	*/
	b _end			/*	error -> terminate	*/

_run :
	bl _setup_pins
	bl _turn_left
	bl _turn_right
	bl _stop
	bl _turn_left
	bl _turn_right
	bl _stop
	
_end:
	pop {lr}
	bx lr

_turn_left :
	push {lr}
	
	ldr r0, =pin_left_a
	bl _write_zero_to_pin

	ldr r0, =pin_left_b
	bl _write_one_to_pin

	ldr r0, =pin_right_a
	bl _write_one_to_pin

	ldr r0, =pin_right_b
	bl _write_zero_to_pin

	bl _delay

	pop {lr}
	bx lr

_turn_right :
	push {lr}
	
	ldr r0, =pin_left_a
	bl _write_one_to_pin

	ldr r0, =pin_left_b
	bl _write_zero_to_pin

	ldr r0, =pin_right_a
	bl _write_zero_to_pin

	ldr r0, =pin_right_b
	bl _write_one_to_pin

	bl _delay

	pop {lr}
	bx lr

_stop :
	push {lr}
	
	ldr r0, =pin_left_a
	bl _write_zero_to_pin

	ldr r0, =pin_left_b
	bl _write_zero_to_pin

	ldr r0, =pin_right_a
	bl _write_zero_to_pin

	ldr r0, =pin_right_b
	bl _write_zero_to_pin

	bl _delay

	pop {lr}
	bx lr

_delay :
	push {lr}
	
	ldr r0, =interval
	ldr r0, [r0]
	bl delay

	pop {lr}
	bx lr

_write_one_to_pin :
	push {lr}

	ldr r0, [r0]
	mov r1, #1
	bl digitalWrite	

	pop {lr}
	bx lr

_write_zero_to_pin :
	push {lr}

	ldr r0, [r0]
	mov r1, #0
	bl digitalWrite	

	pop {lr}
	bx lr

_set_pin_mode :
	push {lr}

	ldr r0, [r0]
	mov r1, #1
	bl pinMode		

	pop {lr}
	bx lr

_setup_pins :
	push {lr}

	ldr r0, =pin_left_a
	bl _set_pin_mode

	ldr r0, =pin_left_b
	bl _set_pin_mode

	ldr r0, =pin_right_a
	bl _set_pin_mode

	ldr r0, =pin_right_b
	bl _set_pin_mode

	pop {lr}
	bx lr


