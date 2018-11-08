
include_directories(./include)

set(EXE_NAME __EXE_NAME__)
set(SOURCES
  src/main.cpp
  )


add_executable(${EXE_NAME} ${SOURCES})
