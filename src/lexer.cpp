#include <iostream>

#include "regex.hpp"
#include "lexer.hpp"

static bool is_whitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n';
}

static bool print_with_space(Token tok) {
    switch (tok) {
    case Token::Colon:
    case Token::Comma:
    case Token::Semicolon:
    case Token::RightBrace:
    case Token::RightBracket:
    case Token::KeywordComp:
        return true;
    default:
        return false;
    }
}

static const char *token_to_string(Token tok) {
    switch (tok) {
    case Token::None: return "None";
    case Token::Unknown: return "Unknown";
    case Token::At: return "At";
    case Token::Colon: return "Colon";
    case Token::ColonEquals: return "ColonEquals";
    case Token::Comma: return "Comma";
    case Token::LessThan: return "LessThan";
    case Token::GreaterThan: return "GreaterThan";
    case Token::LeftParen: return "LeftParen";
    case Token::RightParen: return "RightParen";
    case Token::LeftBracket: return "LeftBracket";
    case Token::RightBracket: return "RightBracket";
    case Token::LeftBrace: return "LeftBrace";
    case Token::RightBrace: return "RightBrace";
    case Token::Plus: return "Plus";
    case Token::Minus: return "Minus";
    case Token::Star: return "Star";
    case Token::Slash: return "Slash";
    case Token::Semicolon: return "Semicolon";
    case Token::RightArrow: return "RightArrow";
    case Token::Number: return "Number";
    case Token::Identifier: return "Identifier";
    case Token::KeywordComp: return "KeywordComp";
    default: return "?";
    }
}

static const char *token_to_symbol(Token tok) {
    switch (tok) {
    case Token::None: return "None";
    case Token::Unknown: return "Unknown";
    case Token::At: return "@";
    case Token::Colon: return ":";
    case Token::ColonEquals: return ":=";
    case Token::Comma: return ",";
    case Token::LessThan: return "<";
    case Token::GreaterThan: return ">";
    case Token::LeftParen: return "(";
    case Token::RightParen: return ")";
    case Token::LeftBracket: return "[";
    case Token::RightBracket: return "]";
    case Token::LeftBrace: return "{";
    case Token::RightBrace: return "}";
    case Token::Plus: return "+";
    case Token::Minus: return "-";
    case Token::Star: return "*";
    case Token::Slash: return "/";
    case Token::Semicolon: return ";";
    case Token::RightArrow: return "->";
    case Token::Number: return "?";
    case Token::Identifier: return "?";
    case Token::KeywordComp: return "comp";
    default: return "?";
    }
}

std::vector<TokenPair> Lexer::lex(const std::string &source) {
    std::vector<TokenPair> tokens {};
    auto rest = std::string_view(source);

    for (std::size_t i = 0; i < rest.length(); ) {
        if (is_whitespace(rest[i])) {
            i++;
            continue;
        }

        switch (rest[i]) {
        case '@': tokens.emplace_back("", Token::At); i++; continue;
        case ':': if (auto match_opt = consume(rest.substr(i), "^:="); match_opt.has_value()) {
            tokens.emplace_back("", Token::ColonEquals);
            i += 2;
        } else {
            tokens.emplace_back("", Token::Colon);
            i++;
        } continue;
        case ',': tokens.emplace_back("", Token::Comma); i++; continue;
        case '<': tokens.emplace_back("", Token::LessThan); i++; continue;
        case '>': tokens.emplace_back("", Token::GreaterThan); i++; continue;
        case '(': tokens.emplace_back("", Token::LeftParen); i++; continue;
        case ')': tokens.emplace_back("", Token::RightParen); i++; continue;
        case '[': tokens.emplace_back("", Token::LeftBracket); i++; continue;
        case ']': tokens.emplace_back("", Token::RightBracket); i++; continue;
        case '{': tokens.emplace_back("", Token::LeftBrace); i++; continue;
        case '}': tokens.emplace_back("", Token::RightBrace); i++; continue;
        case '+': tokens.emplace_back("", Token::Plus); i++; continue;
        case '-': if (auto match_opt = consume(rest.substr(i), "^->"); match_opt.has_value()) {
            tokens.emplace_back("", Token::RightArrow);
            i += 2;
        } else {
            tokens.emplace_back("", Token::Minus);
            i++;
        } continue;
        case '*': tokens.emplace_back("", Token::Star); i++; continue;
        case '/': tokens.emplace_back("", Token::Slash); i++; continue;
        case ';': tokens.emplace_back("", Token::Semicolon); i++; continue;
        }

        if (auto match_opt = consume(rest.substr(i), "^[0-9]+"); match_opt.has_value()) {
            auto [match, match_rest] = match_opt.value();
            tokens.emplace_back(std::string(match), Token::Number);
            rest = match_rest;
            i = 0;
            continue;
        } else if (auto match_opt = consume(rest.substr(i), "^(comp)[^a-zA-Z0-9_]"); match_opt.has_value()) {
            auto [match, match_rest] = match_opt.value();
            tokens.emplace_back("", Token::KeywordComp);
            rest = match_rest;
            i = 0;
            continue;
        } else if (auto match_opt = consume(rest.substr(i), "^[a-zA-Z_][a-zA-Z0-9_]*"); match_opt.has_value()) {
            auto [match, match_rest] = match_opt.value();
            tokens.emplace_back(std::string(match), Token::Identifier);
            rest = match_rest;
            i = 0;
            continue;
        }

        tokens.emplace_back(std::string { rest[i] }, Token::Unknown);
        i++;
    }

    return tokens;
}

void Lexer::print_tokens(const std::vector<TokenPair> &tokens) const noexcept {
    for (auto &&[str, tok] : tokens) {
        if (str.size() > 0) {
            std::cout << "<'" << str << "', " << token_to_string(tok) << ">, ";
        } else {
            std::cout << "<" << token_to_string(tok) << ">, ";
        }
    }

    std::cout << '\n';
}

void Lexer::print_symbols(const std::vector<TokenPair> &tokens) const noexcept {
    for (auto &&[str, tok] : tokens) {
        if (tok == Token::Identifier || tok == Token::Number) {
            std::cout << str;
        } else {
            std::cout << token_to_symbol(tok);

            if (print_with_space(tok)) {
                std::cout << ' ';
            }
        }
    }

    std::cout << '\n';
}