cmake_minimum_required(VERSION 3.16)
project(login_server)
set(CMAKE_CXX_STANDARD 20)

# Optional: Fetch Catch2
include(FetchContent)
FetchContent_Declare(
    catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.5.3
)
FetchContent_MakeAvailable(catch2)

# Include headers
include_directories(include)

# Build core service lib
add_library(login_service
    src/UserService.cpp
)

target_include_directories(login_service PUBLIC include)

# Tests
add_executable(login_tests
    tests/test_registration.cpp
    tests/test_login.cpp
)

target_link_libraries(login_tests PRIVATE login_service Catch2::Catch2WithMain)

