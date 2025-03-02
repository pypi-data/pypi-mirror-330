cmake_minimum_required(VERSION 3.16...3.31)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

message(STATUS "sentry-crashpad-handler-wheel version: ${SKBUILD_PROJECT_VERSION}")
string(REGEX MATCH "^([0-9]+)\.([0-9]+)\.([0-9]+)" CRASHPAD_HANDLER_VERSION "${SKBUILD_PROJECT_VERSION}")
message(STATUS "crashpad_handler version: ${CRASHPAD_HANDLER_VERSION}")

set(CMAKE_CXX_STANDARD 20)

# Define a build rule
set(SENTRY_DOWNLOAD_URL "https://github.com/getsentry/sentry-native/releases/download/${CRASHPAD_HANDLER_VERSION}/sentry-native.zip")
include(ExternalProject)
if (WIN32)
    set(CRASHPAD_HANDLER_BUILD_COMMAND ${CMAKE_COMMAND} --build . --target crashpad_handler crashpad_wer --config Release)
else ()
    set(CRASHPAD_HANDLER_BUILD_COMMAND ${CMAKE_COMMAND} --build . --target crashpad_handler --config Release)
endif ()
ExternalProject_add(build-crashpad-handler
        URL "${SENTRY_DOWNLOAD_URL}"
        SOURCE_DIR ${CMAKE_BINARY_DIR}/sentry-native
        BINARY_DIR ${CMAKE_BINARY_DIR}/sentry
        UPDATE_COMMAND ""
        INSTALL_COMMAND ""
        USES_TERMINAL_DOWNLOAD 1
        USES_TERMINAL_CONFIGURE 1
        USES_TERMINAL_BUILD 1
        CMAKE_ARGS -DCMAKE_BUILD_TYPE=Release -DSENTRY_BACKEND=crashpad
        BUILD_COMMAND ${CRASHPAD_HANDLER_BUILD_COMMAND}
)
set(config-subfolder "")
if (CMAKE_GENERATOR MATCHES "Visual Studio")
    set(config-subfolder "Release")
endif ()
set(crashpad-handler-executable ${CMAKE_BINARY_DIR}/sentry/${config-subfolder}/crashpad_build/handler/crashpad_handler${CMAKE_EXECUTABLE_SUFFIX})

# Reduce the size of the executable by executing strip if it is present on the system
find_program(STRIP_EXECUTABLE strip)
if (STRIP_EXECUTABLE)
    add_custom_target(
            strip-crashpad-handler
            ALL
            COMMAND ${STRIP_EXECUTABLE} ${crashpad-handler-executable}
            COMMENT "Stripping crashpad_handler executable for size reduction"
    )
    add_dependencies(strip-crashpad-handler build-crashpad-handler)
endif ()

# Define an installation rule that copies the executable to our Python package
install(PROGRAMS ${crashpad-handler-executable} DESTINATION sentry_crashpad/data/bin)

if (WIN32)
    set(crashpad-wer-library ${CMAKE_BINARY_DIR}/sentry/${config-subfolder}/crashpad_build/handler/crashpad_wer${CMAKE_SHARED_LIBRARY_SUFFIX})
    install(FILES ${crashpad-wer-library} DESTINATION sentry_crashpad/data/bin)
endif ()
