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
    RightArrow,   /* -> */
    Number,       /* [0-9]+ */
    Identifier,
    KeywordComp,  /* comp */
};

#endif // __TOKENS_HPP__