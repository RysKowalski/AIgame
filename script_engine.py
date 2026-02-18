"""
at the start, script engine will load variables from level
$1 $2 $3 $4 ...
and special variables
$count - count of level variables
$time - current time of the level
$reward - current reward

at the start of execution engine creates special variable $return
$return - value returned by execution
default value is 0
when running as a single line, $return is ignored and instead expression is used directly

variables can be created by writing
variableName = <number|expression>
then variables can be used by using $variableName

expressions
expressions can be used like this:
$return = ($var1 + $var2) * var3
"""
