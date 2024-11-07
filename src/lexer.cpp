#include <iostream>
#include <sstream>

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
    case Token::LeftBrace:
    case Token::RightBracket:
    case Token::KeywordComp:
    case Token::KeywordNew:
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
    case Token::KeywordNew: return "KeywordNew";
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
    case Token::KeywordNew: return "new";
    default: return "?";
    }
}

Token Lexeme::token() const noexcept {
    return _token;
}

int Lexeme::priority() const noexcept {
    return _priority;
}

bool Lexeme::matches(std::string_view str) const noexcept {
    if (const auto match = consume(str, _symbol); match.has_value()) {
        return true;
    }

    return false;
}

std::optional<std::pair<std::string_view, std::size_t>> Lexeme::match(std::string_view str) const noexcept {
    if (const auto match = consume(str, _symbol); match.has_value()) {
        auto [match_str, rest] = match.value();
        return std::make_pair(rest, match_str.size());
    }

    return std::nullopt;
}

void Lexer::add_lexeme(const char *symbol, Token token, int priority) noexcept {
    _lexemes.emplace_back(symbol, token, priority);
}

std::vector<TokenPair> Lexer::lex(const std::string &source) const noexcept {
    std::vector<TokenPair> tokens {};
    auto rest = std::string_view(source);

    for (std::size_t i = 0; i < rest.size(); ) {
        if (is_whitespace(rest[i])) {
            i++;
            continue;
        }

        bool had_match = false;

        /* Try to match the longest possible lexeme. This prevents shorter lexemes,
         * such as `-` from preferentially matching over longer ones like `->`.
         * If two lexemes have the same length, return the lexeme with higher
         * priority. This prevents identifiers from matching over keywords. */
        std::size_t longest_match = 0;
        int highest_priority = 0;
        auto longest_match_token = Token::None;

        for (auto &&lexeme : _lexemes) {
            if (auto match = lexeme.match(rest.substr(i)); match.has_value()) {
                had_match = true;
                auto [new_rest, match_len] = match.value();

                if (match_len > longest_match) {
                    longest_match = match_len;
                    longest_match_token = lexeme.token();
                    highest_priority = lexeme.priority();
                } else if (match_len == longest_match && lexeme.priority() > highest_priority) {
                    highest_priority = lexeme.priority();
                    longest_match_token = lexeme.token();
                }
            }
        }

        if (!had_match) {
            std::cout << "TokenError at " << i << ": '" << rest[i] << "'\n";
            break;
        } else {
            tokens.emplace_back(rest.substr(i, longest_match), longest_match_token);
            i += longest_match;
        }
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

std::string Lexer::symbols_string(const std::vector<TokenPair> &tokens) const noexcept {
    std::stringstream ss;

    for (std::size_t i = 0; i < tokens.size(); i++) {
        const auto &[str, tok] = tokens[i];

        if (tok == Token::Identifier || tok == Token::Number) {
            ss << str;
            if (i + 1 < tokens.size() && tokens[i+1].second == Token::Identifier) {
                ss << ' ';
            }
        } else {
            ss << token_to_symbol(tok);

            if (print_with_space(tok)) {
                ss << ' ';
            }
        }
    }

    return ss.str();
}

void Lexer::print_symbols(const std::vector<TokenPair> &tokens) const noexcept {
    std::cout << this->symbols_string(tokens) << '\n';
}