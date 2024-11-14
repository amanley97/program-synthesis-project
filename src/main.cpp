#include <iostream>
#include <string>
#include <vector>

#include <z3++.h>

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

void demorgan() {
    using namespace z3;
    std::cout << "de-Morgan example\n";
    
    context c;

    expr x = c.bool_const("x");
    expr y = c.bool_const("y");
    expr conjecture = (!(x && y)) == (!x || !y);
    
    solver s(c);
    // adding the negation of the conjecture as a constraint.
    s.add(!conjecture);
    std::cout << s << "\n";
    std::cout << s.to_smt2() << "\n";
    switch (s.check()) {
        case unsat:   std::cout << "de-Morgan is valid\n"; break;
        case sat:     std::cout << "de-Morgan is not valid\n"; break;
        case unknown: std::cout << "unknown\n"; break;
    }
}

int main(int argc, char *argv[]) {
    demorgan();

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
