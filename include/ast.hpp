/**
 * \file ast.hpp
 */

#ifndef __AST_HPP__
#define __AST_HPP__

#include <string>
#include <utility>
#include <vector>

/**
 * \class ASTNode
 */
class ASTNode {

};


class Port : public ASTNode {
protected:
    std::string _name {};
};

class ControlPort final : public Port {}; // port defined with the `interface` keyword

class DataPort final : public Port { // any other port is a data port
private:
    std::pair<std::size_t, std::size_t> _availability_interval {};
};


class Expression : public ASTNode {};

// x ? y : z
class IfThenElseExpr : public Expression {};

// x == y
class BoolEqualsExpr : public Expression {};

// x + y
class AdditionExpr : public Expression {};

// x - y
class SubtractionExpr : public Expression {};

// x * y
class MultiplicationExpr : public Expression {};

// x / y
class DivisionExpr : public Expression {};

// x % y
class ModulusExpr : public Expression {};

// new Comp;
class GetComponentExpr final : public Expression {};

// A<G + n>(...);
class InvocationExpr final : public Expression {};


class Command : public ASTNode {

};

// `X := ...`
class InstantiationCmd final : public Command {

};

// `X.y = ...`
class AssignmentCmd final : public Command {

};

// `port = port`
class ConnectionCmd final : public Command {

};


class Component final : public ASTNode {
private:
    std::vector<Port*> _in_ports {};
    std::vector<Port*> _out_ports {};
    std::vector<Command*> _commands {};
};

/**
 * \class ComponentBuilder
 * \brief Used to construct components
 */
class ComponentBuilder {};

#endif // __AST_HPP__

/*
comp Square<T:1>(
    @[T, T+1] left: 32,
    @[T, T+1] right: 32
) -> (
    @[T+1, T+2] out: 32)
{
    M := new Mult;
    m0 := M<G>(l, r)
    m1 := M<G+1>(m0.out, m0.out)
}

Component square = new ComponentBuilder("Square")
    .set_guard("T")
    .add_in_data_port(builder.guard(), builder.guard() + 1, "left", 32)
    .add_in_data_port(builder.guard(), builder.guard() + 1, "right", 32)
    .add_out_data_port(builder.guard() + 1, builder.guard() + 2, "out", 32)
    .add_command(new GetInstance("M", "Mult")) // M := Mult;
    .add_command(new Assignment("m0", new Invocation("M", builder.guard(), "l", "r")))
    .add_command(new Assignment("m1", new Invocation("M", builder.guard() + 1, "m0.out", "m0.out")))
    .build();
*/
