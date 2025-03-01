cmake_minimum_required(VERSION 3.22)
project(vidur_example LANGUAGES CXX)

################################################################################
# Build Settings
################################################################################
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

################################################################################
# Find Vidur Library
################################################################################

# Function to find Python site-packages directory
function(find_python_site_packages_dir result)
    execute_process(
        COMMAND python3 -c "import site; print(site.getsitepackages()[0])"
        OUTPUT_VARIABLE SITE_PACKAGES_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    set(${result} ${SITE_PACKAGES_DIR} PARENT_SCOPE)
endfunction()

# Get site-packages directory
find_python_site_packages_dir(PYTHON_SITE_PACKAGES)

# Set Vidur paths
set(VIDUR_LIBRARY ${PYTHON_SITE_PACKAGES}/vidur/lib/libvidur.so)
set(VIDUR_INCLUDE_DIR ${PYTHON_SITE_PACKAGES}/vidur/lib/include)

# Verify paths exist
if(NOT EXISTS ${VIDUR_LIBRARY})
    message(FATAL_ERROR "Vidur library not found at: ${VIDUR_LIBRARY}")
endif()

if(NOT EXISTS ${VIDUR_INCLUDE_DIR})
    message(FATAL_ERROR "Vidur include directory not found at: ${VIDUR_INCLUDE_DIR}")
endif()

################################################################################
# Example Target
################################################################################

# Create config_test executable
add_executable(config_test config_test.cpp)

# Add include directories
target_include_directories(config_test PRIVATE ${VIDUR_INCLUDE_DIR})

# Link against Vidur library
target_link_libraries(config_test PRIVATE ${VIDUR_LIBRARY})