#include <iostream>
#include <string>
#include <vector>

#include "regex.hpp"
#include "tokens.hpp"
#include "lexer.hpp"

auto src = "comp Add<G>(); comp Mul<G>();\n"
           "comp Alu<G>(\n"
           "    @[G,G+1] op: 32,\n"
           "    @[G,G+1] l: 32,\n"
           "    @[G,G+1] r: 32\n"
           ") -> (\n"
           "    @[G,G+1] out: 32\n"
           ") {"
           "    A := new Add;\n"
           "    a0 := A<G+n>(l, r);\n"
           "}\n";

int main(int argc, char *argv[]) {
    Lexer lexer;
    set_up_lexer_for_filament(lexer);

    for (;;) {
        std::string line;
        std::getline(std::cin, line);

        if (line.size() == 0) {
            break;
        }

        std::cout << "\"" << line << "\" -> ";

        const auto tokens = lexer.lex(line);
        lexer.print_tokens(tokens);
        lexer.print_symbols(tokens);
    }

    const auto tokens = lexer.lex(src);
    // lexer.print_tokens(tokens);
    lexer.print_symbols(tokens);

    return 0;
}