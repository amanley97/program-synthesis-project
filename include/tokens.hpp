/**
 * \file tokens.hpp
 * \author Harlan Williams <hrw@ku.edu>
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
    Semicolon,    /*  ; */
    Period,       /*  . */
    RightArrow,   /* -> */
    Number,       /* [0-9]+ */
    Identifier,
    KeywordComp,  /* comp */
    KeywordNew,   /* new */
    KeywordInterface,  /* interface */
    KeywordExtern,     /* extern */
};

bool print_with_space(Token tok);
const char *token_to_string(Token tok);
const char *token_to_symbol(Token tok);

#endif // __TOKENS_HPP__