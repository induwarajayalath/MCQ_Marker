#include <stdio.h>

int main(int argc, char const *argv[])
{
    printf("Hello World three");
    if (3<5)
    {
        int i = 0;
        while (i < 5) {
            printf("%d\n", i);
            i++;
        }

        for (i = 1; i < 11; ++i)
        {
            printf("%d ", i);
        }
        printf("Answer Printed");
    }
    
    return 0;
}
