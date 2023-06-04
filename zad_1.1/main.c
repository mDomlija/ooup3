#include "myfactory.h"
#include <alloca.h>
#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

struct Animal{
    PTRFUN* vtable;
    // vtable entries:
    // 0: char const* name(void* this);
    // 1: char const* greet();
    // 2: char const* menu();
};

// parrots and tigers defined in respective dynamic libraries

// animalPrintGreeting and animalPrintMenu similar as in lab 1
void animalPrintGreeting(struct Animal* a){
    printf("%s pozdravlja: %s\n", a->vtable[0](a), a->vtable[1]());
}

void animalPrintMenu(struct Animal* a){
    printf("%s voli %s\n", a->vtable[0](a), a->vtable[2]());
}

int main(int argc, char *argv[]){

    printf("NA GOMILI:\n");
    for (int i=0; i<argc/2; ++i){
        struct Animal* p=(struct Animal*)myfactory(argv[1+2*i], argv[1+2*i+1]);
        if (!p){
            printf("Creation of plug-in object %s failed.\n", argv[1+2*i]);
            continue;
        }

        animalPrintGreeting(p);
        animalPrintMenu(p);
        free(p); 
    }

    printf("\nNA STOGU:\n");
    for (int i=0; i<argc/2; ++i){
        size_t size = myfactory_sizeof(argv[1+2*i]);
        struct Animal* animal = alloca(size);

        myfactory_construct(animal, argv[1+2*i], argv[1+2*i+1]);
        animalPrintGreeting(animal);
        animalPrintMenu(animal);
    }
}
