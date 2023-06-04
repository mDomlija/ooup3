import os
from importlib import import_module

def printGreeting(pet):
    print(f"{pet.name} pozdravlja: {pet.greet()}")  

def printMenu(pet):
    print(f"{pet.name} voli {pet.menu()}.")

def myfactory(moduleName):
    module=import_module('plugins.'+moduleName)
    return getattr(module, moduleName.capitalize())

def test():
    pets=[]
    # obiđi svaku datoteku kazala plugins 
    for mymodule in os.listdir('plugins'):
        moduleName, moduleExt = os.path.splitext(mymodule)
        # ako se radi o datoteci s Pythonskim kodom ...
        if moduleExt=='.py':
            # instanciraj ljubimca ...
            ljubimac=myfactory(moduleName)('Ljubimac '+str(len(pets)))
            # ... i dodaj ga u listu ljubimaca
            pets.append(ljubimac)

    # ispiši ljubimce
    for pet in pets:
        printGreeting(pet)
        printMenu(pet)

if __name__ == '__main__':
    test()