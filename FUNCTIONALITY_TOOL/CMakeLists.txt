cmake_minimum_required(VERSION 3.15)
project(FunctionalityTool)

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter)

# Directories
set(UI_DIR ${CMAKE_SOURCE_DIR}/ui)
set(SRC_DIR ${CMAKE_SOURCE_DIR}/src)

# Collect all .ui files
file(GLOB UI_FILES "${UI_DIR}/*.ui")

# Compile .ui -> _ui.py
set(UI_PY_FILES "")
foreach(ui_file ${UI_FILES})
    get_filename_component(fname ${ui_file} NAME_WE)
    set(py_file ${SRC_DIR}/${fname}_ui.py)
    add_custom_command(
        OUTPUT ${py_file}
        COMMAND ${Python3_EXECUTABLE} -m PyQt5.uic.pyuic ${ui_file} -o ${py_file}
        DEPENDS ${ui_file}
        COMMENT "Compiling ${ui_file} -> ${py_file}"
    )
    list(APPEND UI_PY_FILES ${py_file})
endforeach()

# Target to build all UI files
add_custom_target(build_ui ALL DEPENDS ${UI_PY_FILES})

# Target to run the application
add_custom_target(run
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/main.py
    DEPENDS build_ui
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running FunctionalityTool..."
)
