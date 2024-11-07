/**
 * \file lexer.hpp
 * \author Harlan Williams <hrw@ku.edu>
 */

#ifndef __LEXER_HPP__
#define __LEXER_HPP__

#include <optional>
#include <string>
#include <utility>
#include <vector>

#include "tokens.hpp"

using TokenPair = std::pair<std::string, Token>;

class Lexeme {
public:
    Lexeme(const char *symbol, Token token, int priority)
        : _symbol(std::string("^") + std::string(symbol)), _token(token), _priority(priority) {}
    Token token() const noexcept;
    int priority() const noexcept;
    bool matches(std::string_view str) const noexcept;
    std::optional<std::pair<std::string_view, std::size_t>> match(std::string_view str) const noexcept;
private:
    std::string _symbol;
    Token _token;
    int _priority;
};

/**
 * \class Lexer
 */
class Lexer {
public:
    void add_lexeme(const char *symbol, Token token, int priority = 0) noexcept;

    /**
     * \brief Takes a string and converts symbols, identifiers, and numbers into a vector of `TokenPairs`, which are defined as
     * `std::pair<std::string, Token>`. These token pairs contain symbols, identifiers, and numbers to be used by the parser to
     * transform source code into an abstract syntax tree (AST) representation.
     * 
     * \param source The source code to be tokenized.
     * \return A `vector<TokenPair>` of token pairs derived from the source code string.
     */
    std::vector<TokenPair> lex(const std::string &source) const noexcept;

    /**
     * \brief Prints a list of token pairs as token names and optional identifiers or numbers for debugging purposes.
     * 
     * \param tokens List of token pairs to print as tokens.
     */
    void print_tokens(const std::vector<TokenPair> &tokens) const noexcept;

    /**
     * \brief Returns a string from a list of token pairs as the symbols they represent and optional identifiers or numbers for
     * debugging purposes. Lexing the string derived from this function and calling this on the new token pair list should result
     * in the exact same string out again.
     * 
     * \param tokens List of token pairs to print to a string.
     * \return A `string` which should appear as a compactified, single-line version of the input.
     */
    std::string symbols_string(const std::vector<TokenPair> &tokens) const noexcept;

    /**
     * \brief Prints a list of token pairs as the symbols they represent and optional identifiers or numbers for debugging purposes.
     * 
     * \param tokens List of token pairs to print as symbols.
     */
    void print_symbols(const std::vector<TokenPair> &tokens) const noexcept;
private:
    std::vector<Lexeme> _lexemes {};
};

#endif // __LEXER_HPP__