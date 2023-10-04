import ctypes
clibrary = ctypes.CDLL(r"C:\<__full_path_to_clibrary.dll__>\clibrary.dll")
clibrary.display()

# Should be working but doesnt work at Windows, libraries for 64 bit only for 32 bit.
# At Linux using gcc and .so files works fine...

# https://www.youtube.com/watch?v=neexS0HK9TY