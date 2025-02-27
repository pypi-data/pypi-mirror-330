"""Binary operations

The `BOp` is the core data structure of snakeHDL. Each `BOp` represents
a low-level primitive binary operation that must be implemented in hardware
by the compiler backends.

`BOp` objects are immutable. They should not be modified by the user
after initialization.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import numpy as np


class BOps(Enum):
  """Enum representing specific types of primitive binary operations.
  """

  # I/O operations
  INPUT = auto()
  OUTPUT = auto()
  CONST = auto()
  BIT = auto()
  JOIN = auto()

  # Combinational operations
  NOT = auto()
  AND = auto()
  NAND = auto()
  OR = auto()
  NOR = auto()
  XOR = auto()
  XNOR = auto()

  def __str__(self) -> str: return super().__str__().split('.')[1]

class BOpGroup:
  """Utility class for grouping related `BOps`.
  """
  IO = {BOps.INPUT, BOps.OUTPUT, BOps.CONST, BOps.BIT, BOps.JOIN}
  COMBINATIONAL = {BOps.NOT, BOps.AND, BOps.NAND, BOps.OR, BOps.NOR, BOps.XOR, BOps.XNOR}

@dataclass(frozen=True)
class BOp:
  """Primitive binary operations that must be implemented in hardware.

  Users should not instantiate `BOp` objects directly, but rather create
  them through the API functions available in this module.
  """

  op: BOps
  src: tuple[BOp, ...] = tuple()
  _bits: Optional[int] = field(default=None)
  _hash: int = 0

  # only for INPUT
  input_name: Optional[str] = None

  # only for OUTPUT
  outputs: Optional[dict[str, BOp]] = None

  # only for CONST
  val: Optional[np.uint] = None

  # only for BIT
  bit_index: Optional[int] = None

  def __post_init__(self):
    object.__setattr__(self, '_hash', hash((
      self.op,
      tuple(id(v) for v in self.src),
      self._bits,
      self.input_name,
      self.val,
      self.bit_index,
    )))

  def __hash__(self) -> int: return self._hash

  def pretty(self, indent: int=0, whitespace: bool=False) -> str:
    sep = '  ' if whitespace else ''
    nl = '\n' if whitespace else ''
    out = indent*sep + _BOP_FUNCS[self.op].__name__ + '('
    if self.op is BOps.INPUT or self.op is BOps.CONST:
      out += nl + (indent+1)*sep + f'bits={self._bits},'
      if self.op is BOps.INPUT: out += nl + (indent+1)*sep + f'name="{self.input_name}",'
      elif self.op is BOps.CONST: out += nl + (indent+1)*sep + f'val={self.val},'
    elif self.op is BOps.OUTPUT:
      if self.outputs is not None:
        for k,v in self.outputs.items(): out += nl + (indent+1)*sep + f'{k}={v.pretty(indent=indent + 2, whitespace=whitespace)},'
    else:
      for v in self.src: out += nl + f'{v.pretty(indent=indent + 1, whitespace=whitespace)},'
    if self.op is BOps.BIT: out += nl + (indent+1)*sep + f'index={self.bit_index},'
    out += nl + indent*sep + ')'
    return out

  def __repr__(self): return self.pretty()

  def __str__(self): return self.pretty(whitespace=True)

  def _cse_id(self) -> str: return 'shared_' + str(self._hash).replace('-', 'n')

def const_bits(val: np.uint | int, bits: int=1) -> BOp:
  """CONST - constant value

  Args:
    val: The value to assign to this constant.
    bits: The bit width of the constant value.

  Returns:
    A `BOp` representing a constant value with a defined bit width.
  """
  return BOp(BOps.CONST, val=np.uint(val), _bits=bits)

def input_bits(name: str, bits: int=1) -> BOp:
  """INPUT - named circuit input

  Args:
    name: The name to assign to this input. Make sure not to use reserved
      keywords from Verilog or VHDL.
    bits: The bit width of the input.

  Returns:
    A `BOp` representing a named input.
  """
  return BOp(BOps.INPUT, input_name=name, _bits=bits)

def output(**kwargs: BOp) -> BOp:
  """OUTPUT - named circuit output

  Args:
    **kwargs: Each kwarg represents a named output in your circuit. Make sure
      not to use reserved keywords from Verilog or VHDL.

  Returns:
    A `BOp` representing a collection of named outputs.
  """
  return BOp(BOps.OUTPUT, outputs=kwargs)

def bit(src: BOp, index: int) -> BOp:
  """BIT - select one bit from `src`

  Args:
    src: The `BOp` to select a bit from.
    index: The index of the bit to select (indexed from LSB to MSB).

  Returns:
    A `BOp` representing a bit selected from `src`.
  """
  return BOp(BOps.BIT, src=(src,), bit_index=index)

def join(*args: BOp) -> BOp:
  """JOIN - combine `n` 1-bit signals into one `n`-bit signal

  Args:
    *args: The `BOp` list to join into one signal. Each
      arg must have a bit width of 1.

  Returns:
    A `BOp` of bit width `n`, where `n` is the length of `args`.
  """
  return BOp(BOps.JOIN, src=tuple(args))

def neg(a: BOp) -> BOp:
  """NOT - negation

  Args:
    a: The `BOp` to negate.

  Returns:
    A `BOp` representing the unary operation `NOT a`.
  """
  return BOp(BOps.NOT, src=(a,))

def conj(a: BOp, b: BOp) -> BOp:
  """AND - conjunction

  Args:
    a: The first operand.
    b: The second operand.

  Returns:
    A `BOp` representing the binary operation `a AND b`.
  """
  return BOp(BOps.AND, src=(a,b))

def nand(a: BOp, b: BOp) -> BOp:
  """NAND - non-conjunction

  Args:
    a: The first operand.
    b: The second operand.

  Returns:
    A `BOp` representing the binary operation `a NAND b`.
  """
  return BOp(BOps.NAND, src=(a,b))

def disj(a: BOp, b: BOp) -> BOp:
  """OR - disjunction

  Args:
    a: The first operand.
    b: The second operand.

  Returns:
    A `BOp` representing the binary operation `a OR b`.
  """
  return BOp(BOps.OR, src=(a,b))

def nor(a: BOp, b: BOp) -> BOp:
  """NOR - non-disjunction

  Args:
    a: The first operand.
    b: The second operand.

  Returns:
    A `BOp` representing the binary operation `a NOR b`.
  """
  return BOp(BOps.NOR, src=(a,b))

def xor(a: BOp, b: BOp) -> BOp:
  """XOR - exclusive disjunction

  Args:
    a: The first operand.
    b: The second operand.

  Returns:
    A `BOp` representing the binary operation `a XOR b`.
  """
  return BOp(BOps.XOR, src=(a,b))

def xnor(a: BOp, b: BOp) -> BOp:
  """XNOR - biconditional

  Args:
    a: The first operand.
    b: The second operand.

  Returns:
    A `BOp` representing the binary operation `a XNOR b`.
  """
  return BOp(BOps.XNOR, src=(a,b))

_BOP_FUNCS = {
  BOps.CONST: const_bits,
  BOps.INPUT: input_bits,
  BOps.OUTPUT: output,
  BOps.BIT: bit,
  BOps.JOIN: join,
  BOps.NOT: neg,
  BOps.AND: conj,
  BOps.NAND: nand,
  BOps.OR: disj,
  BOps.NOR: nor,
  BOps.XOR: xor,
  BOps.XNOR: xnor,
}
