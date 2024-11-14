CPP := g++ -std=c++17
OPTFLAGS := -O0
CPPFILES := $(wildcard src/*.cpp)
Z3-BIN := thirdparty/z3-4.13.3-x64-glibc-2.35/bin
Z3-INC := thirdparty/z3-4.13.3-x64-glibc-2.35/include

synthesizer: $(CPPFILES)
	$(CPP) -Wall $(OPTFLAGS) -I./include -I$(Z3-INC) $^ $(Z3-BIN)/libz3.a -o $@

test: src/lexer.cpp src/regex.cpp tests/lexer_test.cpp
	$(CPP) -fprofile-arcs -ftest-coverage -O0 -I./include $^ -o $@
	./$@
	# gcov -pb lexer_test-lexer

docs:
	doxygen

clean:
	-rm -r docs
	-rm *.gcov
	-rm *.gcda
	-rm *.gcno
	-rm synthesizer
	-rm test
