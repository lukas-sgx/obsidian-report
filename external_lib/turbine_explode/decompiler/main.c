/*
** EPITECH PROJECT, 2026
** ~/epitech/delivery/PoC_EPI_OBSIDIAN
** File description:
** main
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    int iVar1;
    size_t sVar2;
    long long lVar3;
    long in_FS_OFFSET;
    char local_98[136];

    printf("Enter the number of degrees you want to increase or decrease the turbine temperature : ");
    fgets(local_98,0x80,stdin);
    sVar2 = strcspn(local_98,"\n");
    local_98[sVar2] = '\0';
    lVar3 = strtoll(local_98,(char **)0x0,10);
    iVar1 = (int)lVar3;
    if ((iVar1 == 0x7ffffffe) || (iVar1 == -0x7fffffff)) {
        puts("Turbine temperature is too unstable.");
        puts("{ERR0R TURBINE WILL EXPLODE}");
        exit(1);
    }
}