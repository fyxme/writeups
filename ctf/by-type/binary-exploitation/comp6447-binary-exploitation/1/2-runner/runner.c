#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(int argc, char* argv[]) {
	char buffer[512];
	setbuf(stdout, NULL);
	printf("Give me exactly 512 bytes of x86 machine code and I'll run it. Simple as that\n");
	read(STDIN_FILENO,buffer,sizeof buffer);
	((void(*)())buffer)(); //CALL buffer
}
