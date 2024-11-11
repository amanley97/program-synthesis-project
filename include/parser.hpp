/**
 * \file parser.hpp
 * \author Harlan Williams <hrw@ku.edu>
 */

/**
 * \page Filament
 * # The Filament language
 * 
 * > [Section 3] Filament only has four constructs: components, instantiation, connections, and invocations. The first three have
 * direct analogues in traditional HDLs while invocations are a novel construct.
 * 
 * ## Events and timelines
 * 
 * > Designs use events to schedule computation. The Filament compiler generates efficient, pipelined finite state
 * machines to reify events 
 * 
 * ### Defining events
 * 
 * > There are only two ways to define events: (1) component signatures bind event
 * variables like `G`, and (2) users can write event expressions such as `G+n` where `n` is a constant.
 * Adding event variables is disallowed.
 * 
 * ### Timeline interpretation of events
 * 
 * ## Components
 * 
 * > Filament programs are organized in terms of components which describe timing behavior in their
 * signatures and their circuit using a set of commands.
 * 
 * ### Interface ports
 * 
 * > Each event may have at most one interface port
 * 
 * > If an event does not have an interface port, then the module can
 * assume that the event triggers every n cycles where n is the event’s delay
 * 
 * ### Availability intervals
 * 
 * ## Instances
 * 
 * ## Invocations
 * 
 * > Every use of an instance in Filament must be explicitly
 * named and scheduled through an invocation. The first invocation of
 * the multiplier `m0 := M<G>(l, r)` is scheduled using the event `G`, uses the inputs `l` and
 * `r`, and is named `m0`. The second invocation, `m1 := M<G+1>(m0.out, m0.out)`, is scheduled one cycle later
 * at `G + 1`, 
 * 
 * ## Connections
 * 
 * ## External components
 * 
 * ### Phantom events
 * 
 * ### Ordering constraints
 * 
 * ### Parametric delays
 * 
 * # The Filament type system
 * 
 */

#ifndef __PARSER_HPP__
#define __PARSER_HPP__

/* grammar:
 * 
 * Statement ::= 'comp' Identifier GuardList ArgumentList ';'
 * 
 * GuardList ::= '<' Identifier (, Identifier)* '>'
 * 
 * ArgumentList ::= '(' ')'
 */

#endif // __PARSER_HPP__