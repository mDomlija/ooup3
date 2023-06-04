#include<stdio.h> 
#include<stdlib.h>
#include<dlfcn.h>
#include<string.h>
#include "myfactory.h"

typedef void* (*PTRFUN)();

const char *getLibname(char const* libname){
    const char *prefix = "./";
    const char *sufix = ".so";
    char *libname2 = malloc(strlen(prefix) + strlen(libname) + strlen(sufix) + 1);
    strcpy(libname2, prefix);
    strcat(libname2, libname);
    strcat(libname2, sufix);
    libname = libname2;
    return libname;
}

size_t myfactory_sizeof(char const* libname){
    libname = getLibname(libname);

    void *lib = dlopen(libname, RTLD_LAZY);
    if (!lib){
        printf("%s\n", dlerror());
        return 0;
    }
    
    void *sizeof_ = dlsym(lib, "sizeof_");
    
    char *error = dlerror();
    if (error != NULL){
        printf("%s\n", error);
        dlclose(lib);
        return 0;
    }

    return ( (size_t (*)())sizeof_ )();
}

void myfactory_construct(void* addr, char const* libname, char const* name){
    libname = getLibname(libname);

    void *lib = dlopen(libname, RTLD_LAZY);
    if (!lib){
        printf("%s\n", dlerror());
        return;
    }
    
    void *construct = dlsym(lib, "construct");
    
    char *error = dlerror();
    if (error != NULL){
        printf("%s\n", error);
        dlclose(lib);
        return;
    }

    return ( (void (*)(void*, char const*))construct )(addr, name);
}

void *myfactory(char const* libname, char const* name){
    libname = getLibname(libname);

    void *lib = dlopen(libname, RTLD_LAZY);
    if (!lib){
        printf("%s\n", dlerror());
        return NULL;
    }
    
    void *create = dlsym(lib, "create");
    
    char *error = dlerror();
    if (error != NULL){
        printf("%s\n", error);
        dlclose(lib);
        return NULL;
    }

    return ( (PTRFUN)create )(name);
}