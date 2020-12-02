#include <string.h>
#include <stdio.h>




void main()
{
    char name = "abc";
    char name2 = "abc";

    int ret = strcmp(name,name2);

    printf("%d", ret);
}
