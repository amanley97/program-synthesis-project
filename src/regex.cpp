#include "regex.hpp"

std::optional<std::pair<std::string_view, std::string_view>> consume(std::string_view str, const std::string &match) {
    Regex re(match);
    auto span = re.match(str);

    if (span.has_value()) {
        auto [start, offset] = span.value();
        return std::pair<std::string_view, std::string_view>(
            str.substr(start, offset),
            str.substr(start + offset)
        );
    }

    return std::nullopt;
}

Regex::Regex(const std::string &expr) {
    if (_regex_cache.find(expr) != _regex_cache.end()) {
        *this = _regex_cache[expr];
    } else {
        bool start_of_expr = true;
        bool explicit_start = false;
        bool escaped = false;

        for (std::size_t i = 0; i < expr.length(); i++) {
            if (expr[i] == '\\') {
                escaped = true;
                start_of_expr = false;
                continue;
            }

            if (escaped) {
                _states.push_back(RegexNode(expr[i]));
                escaped = false;
                continue;
            }

            if (expr[i] == '*' && _states.size() > 0) {
                _states.back().star();
            } else if (expr[i] == '+' && _states.size() > 0) {
                _states.push_back(RegexNode(_states.back()));
                _states.back().star();
            } else if (expr[i] == '(' && !explicit_start) {
                _states.push_back(RegexNode());
                _states.back().start_match();
                explicit_start = true;
            } else if (expr[i] == '[') { // doesn't honor escapes
                _states.push_back(RegexNode());
                i++;

                if (expr[i] == '^') {
                    _states.back().not_in();
                    i++;
                }

                while (i < expr.length() && expr[i] != ']') {
                    if (i+2 < expr.length() && expr[i+1] == '-') {
                        _states.back().add_pair(expr[i], expr[i+2]);
                        i += 3;
                    } else {
                        _states.back().add_pair(expr[i], '\0');
                        i++;
                    }
                }
            } else if (expr[i] == '.') {
                _states.push_back(RegexNode(' ', '~'));
            } else if (expr[i] == '^' && start_of_expr) {
                _caret = true;
            } else {
                _states.push_back(RegexNode(expr[i]));
            }

            start_of_expr = false;
        }

        if (explicit_start) {
            for (std::size_t i = _states.size() - 1; i >= 0; i--) {
                if (_states[i].first_lower() == ')') {
                    _states[i].stop_match();
                    break;
                }
            }
        }

        _regex_cache[expr] = *this;
    }
}

Regex::RegexNode const* Regex::lookahead(const std::vector<Regex::RegexNode> &nodes, std::size_t start) {
    for (std::size_t i = start + 1; i < nodes.size(); i++) {
        if (nodes[i].char_matching()) {
            return &(nodes[i]);
        }
    }

    return nullptr;
}

std::optional<std::pair<std::size_t, std::size_t>> Regex::match(std::string_view str) const {
    std::size_t state_idx = 0;
    std::size_t start_range = 0;
    std::size_t stop_range = 0;
    std::size_t i;

    for (i = 0; i < str.length() && state_idx < _states.size(); i++) {
        if (_states[state_idx].is_star()) {
            while (i < str.length() && !_states[state_idx].transition(str[i])) {
                // lookahead to the next state that can match
                auto next_matching_state = this->lookahead(_states, state_idx);
                if (next_matching_state && next_matching_state->accept(str[i])) {
                    break;
                }

                i++;
            }

            state_idx++;
            i--;
        } else if (_states[state_idx].is_start()) {
            start_range = i;
            state_idx++;
            i--;
        } else if (_states[state_idx].is_stop()) {
            stop_range = i;
            state_idx++;
            i--;
        } else {
            if (_states[state_idx].transition(str[i])) {
                state_idx++;
            } else if (!_caret) {
                state_idx = 0;
                start_range = i+1;
            } else {
                return std::nullopt;
            }
        }
    }

    if (stop_range == 0) {
        stop_range = i;
    }

    if (state_idx == _states.size() || _states[state_idx].is_star() || (state_idx == _states.size() - 1 &&_states[state_idx].is_stop())) {
        return std::make_pair(start_range, stop_range - start_range);
    }

    return std::nullopt;
}

Regex::RegexNode::RegexNode() {}

Regex::RegexNode::RegexNode(char c) {
    this->add_pair(c, '\0');
}

Regex::RegexNode::RegexNode(char c1, char c2) {
    this->add_pair(c1, c2);
}
void Regex::RegexNode::add_pair(char c1, char c2) {
    _ranges.emplace_back(c1, c2);
}

void Regex::RegexNode::star() {
    _star = true;
}

void Regex::RegexNode::start_match() {
    _start = true;
}

void Regex::RegexNode::stop_match() {
    _stop = true;
}

void Regex::RegexNode::not_in() {
    _not = true;
}

char Regex::RegexNode::first_lower() const {
    return _ranges[0].first;
}
char Regex::RegexNode::first_upper() const {
    return _ranges[0].second;
}

bool Regex::RegexNode::is_star() const noexcept {
    return _star;
}

bool Regex::RegexNode::is_start() const noexcept {
    return _start;
}

bool Regex::RegexNode::is_stop() const noexcept {
    return _stop;
}

bool Regex::RegexNode::is_not() const noexcept {
    return _not;
}

bool Regex::RegexNode::char_matching() const noexcept {
    return !_start && !_stop;
}

bool Regex::RegexNode::accept(char c) const {
    for (const auto &[lower, upper] : _ranges) {
        if (upper == '\0') {
            if (c == lower) {
                return true;
            }
        } else {
            if ((c >= lower) && (c <= upper)) {
                return true;
            }
        }
    }

    return false;
}

bool Regex::RegexNode::transition(char c) const {
    bool passed = this->accept(c);

    if (_star || _not) {
        return !passed;
    }

    return passed;
}

std::unordered_map<std::string, Regex> Regex::_regex_cache {};
