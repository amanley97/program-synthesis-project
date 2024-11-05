CPP := g++ -std=c++17
CPPFLAGS := -Wall
CPPFILES := $(wildcard src/*.cpp)

synthesizer: $(CPPFILES)
	$(CPP) $(CPPFLAGS) -I./include $^ -o $@

docs:
	doxygen