/*
** EPITECH PROJECT, 2026
** ~/epitech/delivery/PoC_EPI_OBSIDIAN/init_steam_turbine/decompiler
** File description:
** test
*/

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    time_t tVar1;

    tVar1 = time((time_t *)0x0);
    srand((__u_int)tVar1);
    printf("magix - rand:     %i\n", rand());
    return 0;
}