# cmake_minimum_required(VERSION 3.22.1)
# project(pybindings)
# add_subdirectory(pybind11)
# pybind11_add_module(module_name main.cpp)

cmake_minimum_required(VERSION 3.22.1)
project(pybindings)

# Dodaj subdirectory z Pybind11
add_subdirectory(pybind11)

# Utwórz moduł DLL
pybind11_add_module(module_name main.cpp)

# Ustawienia dla pliku wyjściowego DLL
set_target_properties(module_name PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
                                              SUFFIX "${PYTHON_MODULE_EXTENSION}")
