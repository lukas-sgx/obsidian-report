/*
** EPITECH PROJECT, 2026
** ~/epitech/delivery/PoC_EPI_OBSIDIAN/turbine_remote_acces/decompiler
** File description:
** main
*/

#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>

int main(void)
{
    int iVar1;
    size_t __n;
    long in_FS_OFFSET;
    char local_58 [32];
    char local_38 [40];
    
    strncpy(local_38,"Data/remote_accessXXXXXX",0x19);
    iVar1 = mkstemp(local_38);
    if (iVar1 == -1) {
        puts("Error: Unable to create temporary file.");
    }
    else {
        printf("Temporary file created: %s\n",local_38);
        strncpy(local_58,"{ACCESS_GRANTED}",0x11);
        __n = strlen(local_58);
        write(iVar1,local_58,__n);
        close(iVar1);
        puts("Enabling remote access...");
        sleep(5);
        iVar1 = open(local_38,0);
        if (iVar1 == -1) {
            puts("Error: Temporary file was tampered with or deleted.");
        }
        else {
            unlink(local_38);
        }
    }
    return 0;
}

