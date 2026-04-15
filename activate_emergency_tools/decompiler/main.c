/*
** EPITECH PROJECT, 2026
** ~/epitech/delivery/PoC_EPI_OBSIDIAN/activate_emergency_tools/decompiler
** File description:
** main
*/

#include <stdint.h>
#include <string.h>

void main(void)
{
    int32_t iVar1;
    int64_t iVar2;
    int64_t var_78h;
    
    iVar2 = strcspn(&var_78h, 0x4b004b);
    if ((char)var_78h == '\0') {
        putstr("No password entered, emergency protocols not activated.");
    } else {
        iVar1 = strcmp(&var_78h, "admin123");
        if (iVar1 == 0) {
            putstr("{Emergency protocols activated, you are now admin !}");
        }
    }
    return;
}