/**
 * \file lexer.hpp
 * \author Harlan Williams <hrw@ku.edu>
 */

#ifndef __LEXER_HPP__
#define __LEXER_HPP__

#include <string>
#include <utility>
#include <vector>

#include "tokens.hpp"

using TokenPair = std::pair<std::string, Token>;

/**
 * \class Lexer
 */
class Lexer {
public:
    Lexer() {}
    std::vector<TokenPair> lex(const std::string &source);
    void print_tokens(const std::vector<TokenPair> &tokens) const noexcept;
    void print_symbols(const std::vector<TokenPair> &tokens) const noexcept;
};

#endif // __LEXER_HPP__