/*
** EPITECH PROJECT, 2026
** ~/epitech/delivery/PoC_EPI_OBSIDIAN/run_turbins/decompiler
** File description:
** main
*/

#include <stdlib.h>
#include <stdio.h>

int main(void)

{
    __u_int param2;
    int iVar1;
    size_t sVar2;
    long in_FS_OFFSET;
    __u_int local_a0;
    char local_98 [136];
    
    local_a0 = 0;
    printf("Enter the number of rotation that the turbine will do (between 0 and 15): ");
    fgets(local_98,0x80,stdin);
    sVar2 = strcspn(local_98,"\n");
    local_98[sVar2] = '\0';
    param2 = atoi(local_98);
    if ((param2 == 0) || ((int)param2 < 16)) {
        for (; local_a0 != param2; local_a0 = local_a0 + 1) {
            if (15 < local_a0) {
                puts("{ERR0R TURB1NE CAN\'T ST0P}");
            }
            printf("Turbine is running... %d/%d\n",local_a0 + 1,param2);
            iVar1 = rand();
            sleep(iVar1 % 3 + 1);
        }
        puts("Turbine has stopped.");
    }
    else {
        puts("Invalid number of rotations.");
    }
    return 0;
}