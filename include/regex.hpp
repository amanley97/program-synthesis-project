/// @file regex.hpp

#ifndef __REGEX_HPP__
#define __REGEX_HPP__

#include <optional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

/// @brief Consume part of a string, optionally returning a pair of the (matching substring, the rest of the string)
/// or None if no match was found.
///
/// `match` is an expression in a restricted regex grammar that implements only single capture groups, character
/// classes in square brackets, the `+` and `*` operators, and `^` to represent either the beginning of a string or
/// a `not` in a character class.
/// @param str 
/// @param match 
/// @return `Option[Match, Rest]`
std::optional<std::pair<std::string_view, std::string_view>> consume(std::string_view str, const std::string &match);

class Regex {
public:
    Regex() {}
    Regex(const std::string &expr);
    std::optional<std::pair<std::size_t, std::size_t>> match(std::string_view str) const;
private:
    struct RegexNode {
    public:
        RegexNode();
        RegexNode(char c);
        RegexNode(char c1, char c2);
        void add_pair(char c1, char c2);
        void star();
        void start_match();
        void stop_match();
        void not_in();
        char first_lower() const;
        char first_upper() const;
        bool is_star() const noexcept;
        bool is_start() const noexcept;
        bool is_stop() const noexcept;
        bool is_not() const noexcept;
        bool accept(char c) const;
        bool transition(char c) const;
        bool char_matching() const noexcept;
    protected:
        std::vector<std::pair<char, char>> _ranges {};
        bool _star = false;
        bool _start = false;
        bool _stop = false;
        bool _not = false;
    };

    static Regex::RegexNode const* lookahead(const std::vector<Regex::RegexNode> &nodes, std::size_t start);

    static std::unordered_map<std::string, Regex> _regex_cache;
    std::vector<Regex::RegexNode> _states {};
    bool _caret = false;
};

#endif // __REGEX_HPP__
