#include <stdlib.h>
#include <stdio.h>

typedef char const* (*PTRFUN)();

struct tiger{
    PTRFUN* vtable;
    char const* name;
};

char const* name(void* this){
    return ((struct tiger*)this)->name;
}

char const* greet(){
    return "Mijau!";
}

char const* menu(){
    return "mlako mlijeko";
}

PTRFUN tiger_vtable[3] = { (PTRFUN)name, (PTRFUN)greet, (PTRFUN)menu };

size_t sizeof_(){
    return sizeof(struct tiger);
}

void *construct(void* addr, char const* name){
    struct tiger *t = (struct tiger*)addr;
    t->vtable = tiger_vtable;
    t->name = name;
}

void *create(char const* name){
    struct tiger *t = (struct tiger*)malloc(sizeof(struct tiger));
    t->vtable = tiger_vtable;
    t->name = name;
    return t;
}