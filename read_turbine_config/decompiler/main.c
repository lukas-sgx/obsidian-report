/*
** EPITECH PROJECT, 2026
** ~/epitech/delivery/PoC_EPI_OBSIDIAN/read_turbine_config/decompiler
** File description:
** main
*/

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

int main(void)

{
    size_t sVar1;
    char *pcVar2;
    FILE *__stream;
    long in_FS_OFFSET;
    char local_298[128];
    char local_218[256];
    char local_118[264];

    printf("Enter the configuration file name: ");
    fgets(local_298, 0x80, stdin);
    sVar1 = strcspn(local_298, "\n");
    local_298[sVar1] = '\0';
    pcVar2 = strstr(local_298, "..");
    if (pcVar2 == (char *)0x0)
    {
        snprintf(local_218, 0x100, "Data/%s", local_298);
        __stream = fopen(local_218, "r");
        if (__stream == (FILE *)0x0)
        {
            printf("Error: Unable to open file: %s\n", local_218);
        }
        else
        {
            printf("Reading configuration file: %s\n", local_218);
            while (true)
            {
                pcVar2 = fgets(local_118, 0x100, __stream);
                if (pcVar2 == (char *)0x0)
                    break;
                printf("%s", local_118);
            }
            fclose(__stream);
        }
    }
    else
    {
        puts("Error: Invalid file name.");
    }
    return 0;
}
