#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <limits.h>

#define MAX_NUM_LEN 12
#define HOTSTREAK 3
#define MAX_WINS 16
#define ONE_BILLION 1000000000
#define ROULETTE_SIZE 36
#define ROULETTE_SPINS 128
#define ROULETTE_SLOWS 16
#define NUM_WIN_MSGS 10
#define NUM_LOSE_MSGS 5


#define NUM_SEEDS 5000
int main(int argc, char const *argv[]) {
    srand(atoi(argv[1]));

    for(int i = 0; i < 10; i++) {
        printf("%d\n",(rand() % ROULETTE_SIZE)+1);

        // we need to burn one of the rand as it is used to select from win msg
        // `puts(win_msgs[rand()%NUM_WIN_MSGS]);`
        (void) rand();
    }

    return 0;
}
