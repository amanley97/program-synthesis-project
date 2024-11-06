CPP := g++ -std=c++17
OPTFLAGS := -O0
CPPFILES := $(wildcard src/*.cpp)

synthesizer: $(CPPFILES)
	$(CPP) -Wall $(OPTFLAGS) -I./include $^ -o $@

lexer_test: src/lexer.cpp src/regex.cpp tests/lexer_test.cpp
	$(CPP) -fprofile-arcs -ftest-coverage -O0 -I./include $^ -o $@
	./$@
	# gcov -pb lexer_test-lexer

docs:
	doxygen

clean:
	-rm *.gcov
	-rm *.gcda
	-rm *.gcno
	-rm synthesizer
	-rm lexer_test
