/*This file is part of PROMISE.

	PROMISE is free software: you can redistribute it and/or modify it
	under the terms of the GNU Lesser General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	PROMISE is distributed in the hope that it will be useful, but WITHOUT
	ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
	or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
	Public License for more details.

	You should have received a copy of the GNU Lesser General Public
	License along with PROMISE. If not, see
	<http://www.gnu.org/licenses/>.

Promise v1 was written by Romain Picot
Promise v2 has been written from v1 by Thibault Hilaire and Sara Hoseininasab
Promise v3 has been written from v2 by Thibault Hilaire, Fabienne JÉZÉQUEL and Xinye Chen
	Promise v3 enables version check, pip installing, arbitrary precision, etc., features.
	Sorbonne Université
	LIP6 (Computing Science Laboratory)
	Paris, France. Contact: thibault.hilaire@lip6.fr, fabienne.jezequel@lip6.fr, xinyechenai@gmail.com


Contains some macros used to check the precision (and compare with the expectations):
- PROMISE_CHECK_VAR(v)   to check the value of a variable v
- PROMISE_CHECK_ARRAY(x,n)  to check the values of an array x of size n
- PROMISE_CHECK_ARRAY2D(x,n,m)    to check the values of an 2D-array x of size n by m (added by Xinye Chen, xinyechenai@gmail.com)

THe same as promise.h, but without the function code

© Thibault Hilaire and Fabienne JÉZÉQUEL, April 2024
*/

#ifndef __PROMISE_DUMP_HEADER__
#define __PROMISE_DUMP_HEADER__


#include <stdio.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <stdlib.h>
#include <math.h>

using namespace std;


/* These two macros export the value(s) to check to Promise2
Usage:
- `PROMISE_CHECK_VAR(var);`     to export the variable `var`
- `PROMISE_CHECK_ARRAY(var);`   to exporrt the n values of the array `var`
*/
#define PROMISE_CHECK_VAR(var) promise_dump(#var, &var, 1)
#define PROMISE_CHECK_ARRAY(var, n) promise_dump(#var, (var), n)
#define PROMISE_CHECK_ARRAY2D(var, n, m) promise_dump_arr(#var, (var), n, m)



/* dump (to stdout) a variable:
 - varName: name of the variable dump (obtained with a C macro)
 - a: pointer to the variable (scalar or array) to dump
 - size: size of the array (1 for a scalar)*/
template<typename T>
void promise_dump(char const* varName, T* a, long size);

template<typename T>
void promise_dump_arr(char const* varName, T** a, long rows, long cols);




#ifdef __CADNA__
/* dump (to stdout) a variable, *but* for a stochastic variable:
 - varName: name of the variable dump (obtained with a C macro)
 - a: pointer to the variable (scalar or array) to dump
 - size: size of the array (1 for a scalar)*/
void promise_dump(char const* varName, double_st* a, long size);
void promise_dump_arr(char const* varName, double** a, long rows, long cols);
#endif


#endif
