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

void test_basic_expression(Lexer &lexer) {
    auto tokens = lexer.lex("1 + 2");
    assert(tokens[0].first == "1");
    assert(tokens[0].second == Token::Number);
    assert(tokens[1].first == "+");
    assert(tokens[1].second == Token::Plus);
    assert(tokens[2].first == "2");
    assert(tokens[2].second == Token::Number);
    auto symbols = lexer.symbols_string(tokens);
    assert(symbols == std::string("1+2"));
}

void test_code_snippet(Lexer &lexer) {
    auto tokens = lexer.lex(src);
    auto symbols = lexer.symbols_string(tokens);

    assert(symbols == std::string("comp Add<G>(); comp Mul<G>(); comp Alu<G>(@[G, G+1] op: 32, @[G, G+1] l: 32, @[G, G+1] r: 32)->(@[G, G+1] out: 32){A:=newAdd; a0:=A<G+n>(l, r); } "));
}

int main() {
    Lexer lexer;
    lexer.add_lexeme("@", Token::At);
    lexer.add_lexeme(":", Token::Colon);
    lexer.add_lexeme(":=", Token::ColonEquals);
    lexer.add_lexeme(",", Token::Comma);
    lexer.add_lexeme("<", Token::LessThan);
    lexer.add_lexeme(">", Token::GreaterThan);
    lexer.add_lexeme("\\(", Token::LeftParen);
    lexer.add_lexeme(")", Token::RightParen);
    lexer.add_lexeme("\\[", Token::LeftBracket);
    lexer.add_lexeme("]", Token::RightBracket);
    lexer.add_lexeme("{", Token::LeftBrace);
    lexer.add_lexeme("}", Token::RightBrace);
    lexer.add_lexeme("\\+", Token::Plus);
    lexer.add_lexeme("-", Token::Minus);
    lexer.add_lexeme("\\*", Token::Star);
    lexer.add_lexeme("/", Token::Slash);
    lexer.add_lexeme(";", Token::Semicolon);
    lexer.add_lexeme("->", Token::RightArrow);
    lexer.add_lexeme("[0-9]+", Token::Number);
    lexer.add_lexeme("[a-zA-Z_][a-zA-Z0-9'_]*", Token::Identifier);
    lexer.add_lexeme("comp", Token::KeywordComp, 1);
    lexer.add_lexeme("new", Token::KeywordNew, 1);

    test_basic_expression(lexer);
    test_code_snippet(lexer);
}
