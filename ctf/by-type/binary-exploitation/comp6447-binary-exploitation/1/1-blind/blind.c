#include <stdio.h>
#include <stdlib.h>

void win(void) {
	system("/bin/sh");
}
int main(int argc, char** argv) {
	char buf[64];
	setbuf(stdout, NULL);
	printf("This is almost exactly the same as before...\n");
	gets(buf);
}
