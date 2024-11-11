/**
 * \file tokens.hpp
 * \author Harlan Williams <hrw@ku.edu>
 */

/**
 * \page Tokens
 * # Adding a new token
 * 
 * To add a new token, add its name under the enum class Token in tokens.hpp.
 * 
 * You will then have to add cases to `token_to_string` and `token_to_symbol` for
 * how the token should be displayed, and optionally, if it should be printed with
 * a space after it, to `print_with_space` in tokens.cpp.
 * 
 * Lastly, you will have to add the lexeme in lexer.hpp to `set_up_lexer_for_filament`.
 */

#ifndef __TOKENS_HPP__
#define __TOKENS_HPP__

enum class Token {
    None,
    Unknown,
    At,           /*  @ */
    Colon,        /*  : */
    ColonEquals,  /* := */
    Comma,        /*  , */
    LessThan,     /*  < */
    GreaterThan,  /*  > */
    LeftParen,    /*  ( */
    RightParen,   /*  ) */
    LeftBracket,  /*  [ */
    RightBracket, /*  ] */
    LeftBrace,    /*  { */
    RightBrace,   /*  } */
    Plus,         /*  + */
    Minus,        /*  - */
    Star,         /*  * */
    Slash,        /*  / */
    DoubleSlash,  /*  // */
    Semicolon,    /*  ; */
    Period,       /*  . */
    RightArrow,   /* -> */
    Number,       /* [0-9]+ */
    Identifier,
    KeywordComp,  /* comp */
    KeywordNew,   /* new */
    KeywordInterface,  /* interface */
    KeywordExtern,     /* extern */
    KeywordWhere,      /* where */
};

bool print_with_space(Token tok);
const char *token_to_string(Token tok);
const char *token_to_symbol(Token tok);

#endif // __TOKENS_HPP__