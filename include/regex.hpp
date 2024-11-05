/**
 * \file regex.hpp
 * \author Harlan Williams <hrw@ku.edu>
 */

#ifndef __REGEX_HPP__
#define __REGEX_HPP__

#include <optional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

/**
 * @brief This function handles the creation of compiled regular expressions, and matching, and should be used
 * rather than instantiating a `Regex` directly.
 * 
 * Consumes part of a string, optionally returning a pair of the (matching substring, the rest of the string)
 * or `nullopt` if no match was found.
 * 
 * `match` is an expression in a restricted regex grammar that implements only single capture groups, character
 * classes in square brackets, the `+` and `*` operators, and `^` to represent either the beginning of a string or
 * a `not` in a character class.
 * 
 * @param str 
 * @param match 
 * @return A `pair<string_view, string_view>` consisting of a string view of the matched substring, and the rest
 * of the input string following the match, or `nullopt`.
 */
std::optional<std::pair<std::string_view, std::string_view>> consume(std::string_view str, const std::string &match);

/**
 * \class Regex
 */
class Regex {
public:
    Regex() {}

    /**
     * \brief Compiles a regular expression.
     * \see consume for a description of the regular expression language.
     */
    Regex(const std::string &expr);

    /**
     * \brief Attempt to match a string using the compiled regular expression.
     * 
     * \param str
     * \return A `pair<size_t, size_t>` of starting index, and the length of the match, or `nullopt`.
     */
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
