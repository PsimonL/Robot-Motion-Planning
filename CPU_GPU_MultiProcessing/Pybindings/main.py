# TODO: Cannot find a file.

# import os
# os.add_dll_directory(r"C:\Users\szymo\CLionProjects\untitled\cmake-build-debug\libprinter_stuff.dll")


# import ctypes

# mylibrary = ctypes.CDLL(r'C:\Users\szymo\CLionProjects\untitled\cmake-build-debug\libprinter_stuff.dll')
# mylibrary = ctypes.LibraryLoader(r'C:\Users\szymo\CLionProjects\untitled\cmake-build-debug\libprinter_stuff.dll')

# result = mylibrary.printer()  # Zmień 'nazwa_funkcji' na nazwę funkcji, którą chcesz wywołać
# print("Wynik funkcji:", result)



# import ctypes
# loader = ctypes.LibraryLoader(ctypes.WinDLL if ctypes.windll else ctypes.CDLL)  # Wybiera odpowiednią funkcję w zależności od systemu
#
# mylibrary = loader.LoadLibrary(r'C:\Users\szymo\CLionProjects\untitled\cmake-build-debug\libprinter_stuff.dll')
#
# result = mylibrary.nazwa_funkcji()  # Zmień 'nazwa_funkcji' na nazwę funkcji, którą chcesz wywołać
#
# print("Wynik funkcji:", result)


import module_name

print(module_name.some_fn_python_name(1, 2))

lista = []
lista.appen