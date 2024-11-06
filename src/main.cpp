#include <iostream>
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

    std::cout << "Input:\n" << src << '\n';
    auto tokens = lexer.lex(src);

    std::cout << "\nToken stream:\n";
    lexer.print_tokens(tokens);

    std::cout << "\nTokens to symbols:\n";
    lexer.print_symbols(tokens);

    return 0;
}