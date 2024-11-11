#include "tokens.hpp"

bool print_with_space(Token tok) {
    switch (tok) {
    case Token::DoubleSlash:
    case Token::Colon:
    case Token::Comma:
    case Token::Semicolon:
    case Token::LeftBrace:
    case Token::RightBracket:
    case Token::KeywordComp:
    case Token::KeywordNew:
    case Token::KeywordInterface:
    case Token::KeywordExtern:
    case Token::KeywordWhere:
        return true;
    default:
        return false;
    }
}

const char *token_to_string(Token tok) {
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
    case Token::DoubleSlash: return "DoubleSlash";
    case Token::Semicolon: return "Semicolon";
    case Token::Period: return "Period";
    case Token::RightArrow: return "RightArrow";
    case Token::Number: return "Number";
    case Token::Identifier: return "Identifier";
    case Token::KeywordComp: return "KeywordComp";
    case Token::KeywordNew: return "KeywordNew";
    case Token::KeywordInterface: return "KeywordInterface";
    case Token::KeywordExtern: return "KeywordExtern";
    case Token::KeywordWhere: return "KeywordWhere";
    default: return "?";
    }
}

const char *token_to_symbol(Token tok) {
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
    case Token::DoubleSlash: return "//";
    case Token::Semicolon: return ";";
    case Token::Period: return ".";
    case Token::RightArrow: return "->";
    case Token::Number: return "?";
    case Token::Identifier: return "?";
    case Token::KeywordComp: return "comp";
    case Token::KeywordNew: return "new";
    case Token::KeywordInterface: return "interface";
    case Token::KeywordExtern: return "extern";
    case Token::KeywordWhere: return "where";
    default: return "?";
    }
}