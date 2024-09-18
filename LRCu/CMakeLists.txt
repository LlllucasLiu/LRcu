# cmake needs this line
cmake_minimum_required(VERSION 3.1)

# Enable C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# Define project name
project(test_pro)

set(CMAKE_BUILD_TYPE "Debug")

file(MAKE_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/Modules)

find_package(CUDA REQUIRED)

set(ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)

file(GLOB_RECURSE SRC_TEST ${ROOT_DIR}/*.cpp ${ROOT_DIR}/*.cu)

cuda_add_executable(LRCu ${SRC_TEST} ${SRC_COMMON})
target_link_libraries(LRCu ${OpenCV_LIBRARIES} -lpthread)
target_link_libraries( LRCu  ${CUDA_cublas_LIBRARY} ${CUDA_nppisu_LIBRARY} ${CUDA_nppif_LIBRARY} ${CUDA_nppif_LIBRARY})