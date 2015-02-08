
CC := $(CROSS_COMPILE)gcc
LDFLAGS := -static -Wl,--build-id=none
SRC := src
INCLUDE := include

all:
	$(CC) -fno-builtin -Wall -Wextra -nostdinc -nostdlib -isystem $(O)/include -isystem include $(SRC)/arch-arm/boot.S $(SRC)/arch-arm/main.c -o vh1

run:
	../qemu_mainline/arm-softmmu/qemu-system-arm -kernel vh1 -initrd tools/hyp_ptable -serial stdio -M vexpress-a9 -m 512 -s -S  
