#include <cassert>
#include <iostream>
#include <string>

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

void test_basic_expression() {
    Lexer lexer;
    auto tokens = lexer.lex("1 + 2");
    assert(tokens[0].first == "1");
    assert(tokens[0].second == Token::Number);
    assert(tokens[1].first == "");
    assert(tokens[1].second == Token::Plus);
    assert(tokens[2].first == "2");
    assert(tokens[2].second == Token::Number);
    auto symbols = lexer.symbols_string(tokens);
    assert(symbols == std::string("1+2"));
}

void test_code_snippet() {
    Lexer lexer;
    auto tokens = lexer.lex(src);
    auto symbols = lexer.symbols_string(tokens);

    assert(symbols == std::string("comp Add<G>(); comp Mul<G>(); comp Alu<G>(@[G, G+1] op: 32, @[G, G+1] l: 32, @[G, G+1] r: 32)->(@[G, G+1] out: 32){A:=newAdd; a0:=A<G+n>(l, r); } "));
}

int main() {
    test_basic_expression();
    test_code_snippet();
}
