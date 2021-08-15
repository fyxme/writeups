```
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <seccomp.h>
#include <sys/mman.h>
#include <limits.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>

void setup_seccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    int ret = 0;
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sendfile), 0);
    ret |= seccomp_load(ctx);
    if (ret) {
        exit(1);
    }
}

typedef void (*void_fn)(void);

int main(void) {
    setbuf(stdout, NULL);

    FILE * fptr = fopen("flag.txt","r");
    int fd = fileno(fptr);
    printf("%d\n", fd);
    puts("Goodbye flag!");

    int ret = remove("flag.txt");
    if (ret == 0) {
        puts("Flag file successfully removed.");
    } else {
        puts("Error removing flag file");
        exit(-1);
    }

    puts("What do you have to say about us so carelessly removing your precious flag?");

    void * buf = mmap(0, 4096, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
    void_fn sc = (void_fn) buf;
    ssize_t num_read = read(0, buf, 100);

    setup_seccomp();
    sc();

    return 0;
}
```