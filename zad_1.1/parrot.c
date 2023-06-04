#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

struct parrot{
    PTRFUN* vtable;
    char const* name;
};

char const* name(void* this){
    return ((struct parrot*)this)->name;
}

char const* greet(){
    return "Sto mu gromova!";
}

char const* menu(){
    return "brazilske orahe";
}

PTRFUN parrot_vtable[3] = { (PTRFUN)name, (PTRFUN)greet, (PTRFUN)menu };

size_t sizeof_(){
    return sizeof(struct parrot);
}

void construct(void* addr, char const* name){
    struct parrot *p = (struct parrot*)addr;
    p->vtable = parrot_vtable;
    p->name = name;
}

void *create(char const* name){
    struct parrot *p = (struct parrot*)malloc(sizeof(struct parrot));
    p->vtable = parrot_vtable;
    p->name = name;
    return p;
}