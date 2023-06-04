#include<dlfcn.h>
#include<string.h>
#include<stdlib.h>

void* myfactory(char const* libname, char const* name);
void myfactory_construct(void* addr, char const* libname, char const* name);
size_t myfactory_sizeof(char const* libname);