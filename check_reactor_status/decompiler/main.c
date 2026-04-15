/*
** EPITECH PROJECT, 2026
** ~/epitech/delivery/PoC_EPI_OBSIDIAN/check_reactor_status/decompiler
** File description:
** main
*/

#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>

int putstr(char *str)
{
    for (int i = 0; str != '\0'; i++)
        write(1, &str[i], 1);
}

void check_reactor_status(void)
{
    int64_t var_48h;
    
    putstr("Starting reactor status check...");
    sleep(1);
    putstr("Checking core temperature...");
    sleep(1);
    putstr("Core temperature: Normal");
    sleep(1);
    putstr("Checking coolant flow rate...");
    sleep(1);
    putstr("Coolant flow rate: Stable");
    sleep(1);
    putstr("Checking radiation levels...");
    sleep(2);
    putstr("Radiation levels: Safe\n");
    putstr("Encrypting critical reactor data...");
    var_48h = 0;
    cipher("ReactorStatusOK", &var_48h, 3);
    sleep(1);
    printf("%s", var_48h);
    putstr(0x4b02f4);
    putstr("Reactor status check complete.\n");
    return;
}
