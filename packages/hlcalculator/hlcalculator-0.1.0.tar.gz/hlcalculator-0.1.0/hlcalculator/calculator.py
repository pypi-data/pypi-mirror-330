"""
核心计算器实现，包含科学计算功能

主要功能:
1. 基础运算: 加减乘除、幂运算
2. 科学运算: 平方根、对数、三角函数、阶乘
3. 数学常数: π、e、τ等

示例:
    # 基础运算
    calc = ScientificCalculator()
    calc.calculate('+', 1, 2)      # 返回: 3.0
    calc.calculate('*', 3, 4)      # 返回: 12.0

    # 科学运算
    calc.calculate('sqrt', 16)     # 返回: 4.0
    calc.calculate('sin', 0.5)     # 返回: 0.479425538604203

    # 数学常数
    calc.get_constant('pi')        # 返回: 3.141592653589793
"""
import math
import operator
from typing import Callable, Dict, Union, Any
from decimal import Decimal, InvalidOperation

Number = Union[int, float, Decimal]


class ScientificCalculator:
  """Advanced calculator with scientific operations."""

  # 数学常数定义
  CONSTANTS = {
    'pi': math.pi,  # 圆周率 π
    'e': math.e,  # 自然对数的底数 e
    'tau': math.tau,  # τ = 2π
    'inf': math.inf,  # 无穷大
  }

  @staticmethod
  def add(x: Number, y: Number) -> float:
    """加法运算

    参数:
        x: 第一个数
        y: 第二个数

    返回:
        两数之和

    示例:
        add(1, 2) -> 3.0
        add(-1, 5) -> 4.0
    """
    return float(x) + float(y)

  @staticmethod
  def subtract(x: Number, y: Number) -> float:
    """减法运算

    参数:
        x: 被减数
        y: 减数

    返回:
        两数之差

    示例:
        subtract(5, 3) -> 2.0
        subtract(10, 15) -> -5.0
    """
    return float(x) - float(y)

  @staticmethod
  def multiply(x: Number, y: Number) -> float:
    """乘法运算

    参数:
        x: 第一个因数
        y: 第二个因数

    返回:
        两数之积

    示例:
        multiply(4, 3) -> 12.0
        multiply(2.5, 2) -> 5.0
    """
    return float(x) * float(y)

  @staticmethod
  def divide(x: Number, y: Number) -> float:
    """除法运算

    参数:
        x: 被除数
        y: 除数（不能为0）

    返回:
        两数之商

    异常:
        ValueError: 当除数为0时抛出

    示例:
        divide(10, 2) -> 5.0
        divide(7, 2) -> 3.5
    """
    if float(y) == 0:
      raise ValueError("Division by zero is not allowed")
    return float(x) / float(y)

  @staticmethod
  def power(x: Number, y: Number) -> float:
    """幂运算

    参数:
        x: 底数
        y: 指数

    返回:
        x的y次方

    异常:
        ValueError: 当结果过大无法计算时抛出

    示例:
        power(2, 3) -> 8.0
        power(10, 2) -> 100.0
    """
    try:
      return float(pow(float(x), float(y)))
    except OverflowError:
      raise ValueError("Result too large to compute")

  @staticmethod
  def sqrt(x: Number) -> float:
    """平方根运算

    参数:
        x: 被开方数（必须为非负数）

    返回:
        x的平方根

    异常:
        ValueError: 当输入为负数时抛出

    示例:
        sqrt(16) -> 4.0
        sqrt(2) -> 1.4142135623730951
    """
    if float(x) < 0:
      raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(float(x))

  @staticmethod
  def log(x: Number, base: Number = math.e) -> float:
    """对数运算

    参数:
        x: 真数（必须为正数）
        base: 底数（默认为自然对数的底e）

    返回:
        以base为底x的对数

    异常:
        ValueError: 当真数不为正数或底数不合法时抛出

    示例:
        log(100, 10) -> 2.0  # 以10为底100的对数
        log(2.718281828459045) -> 1.0  # 自然对数
    """
    if float(x) <= 0:
      raise ValueError("Cannot calculate logarithm of non-positive number")
    if float(base) <= 0 or float(base) == 1:
      raise ValueError("Invalid logarithm base")
    return math.log(float(x), float(base))

  @staticmethod
  def sin(x: Number) -> float:
    """正弦函数

    参数:
        x: 角度（弧度制）

    返回:
        x的正弦值

    示例:
        sin(math.pi/2) -> 1.0
        sin(0) -> 0.0
    """
    return math.sin(float(x))

  @staticmethod
  def cos(x: Number) -> float:
    """余弦函数

    参数:
        x: 角度（弧度制）

    返回:
        x的余弦值

    示例:
        cos(math.pi) -> -1.0
        cos(0) -> 1.0
    """
    return math.cos(float(x))

  @staticmethod
  def tan(x: Number) -> float:
    """正切函数

    参数:
        x: 角度（弧度制）

    返回:
        x的正切值

    示例:
        tan(math.pi/4) -> 1.0
        tan(0) -> 0.0
    """
    return math.tan(float(x))

  @staticmethod
  def factorial(x: Number) -> float:
    """阶乘运算

    参数:
        x: 要计算阶乘的数（必须为非负整数）

    返回:
        x的阶乘

    异常:
        ValueError: 当输入为负数或非整数时抛出

    示例:
        factorial(5) -> 120.0
        factorial(0) -> 1.0
    """
    n = int(float(x))
    if n < 0:
      raise ValueError("Cannot calculate factorial of negative number")
    if n != float(x):
      raise ValueError("Factorial only defined for integers")
    return float(math.factorial(n))

  @classmethod
  def get_constant(cls, name: str) -> float:
    """获取数学常数值

    参数:
        name: 常数名称（如'pi', 'e', 'tau'等）

    返回:
        对应的常数值

    异常:
        ValueError: 当常数名称未知时抛出

    示例:
        get_constant('pi') -> 3.141592653589793
        get_constant('e') -> 2.718281828459045
    """
    if name not in cls.CONSTANTS:
      raise ValueError(f"Unknown constant: {name}")
    return cls.CONSTANTS[name]

  # 支持的运算符和对应的处理函数映射
  OPERATIONS: Dict[str, Callable[..., float]] = {
    '+': add,  # 加法
    '-': subtract,  # 减法
    '*': multiply,  # 乘法
    '/': divide,  # 除法
    '^': power,  # 幂运算
    'sqrt': sqrt,  # 平方根
    'log': log,  # 对数
    'sin': sin,  # 正弦
    'cos': cos,  # 余弦
    'tan': tan,  # 正切
    'factorial': factorial,  # 阶乘
  }

  @classmethod
  def calculate(cls, operation: str, *args: Number) -> float:
    """执行指定的计算操作

    这是计算器的主要接口，根据提供的运算符和参数执行相应的计算。

    参数:
        operation: 运算符（如'+', '-', 'sqrt'等，或以'const:'开头获取常数）
        *args: 运算参数（数量取决于具体运算）

    返回:
        计算结果

    异常:
        ValueError: 当运算符未知或参数数量不正确时抛出

    示例:
        # 基础运算
        calculate('+', 1, 2) -> 3.0
        calculate('*', 4, 5) -> 20.0

        # 科学运算
        calculate('sqrt', 16) -> 4.0
        calculate('log', 100, 10) -> 2.0

        # 获取常数
        calculate('const:pi') -> 3.141592653589793
    """
    if operation.startswith('const:'):
      if len(args) != 0:
        raise ValueError("Constants don't take arguments")
      return cls.get_constant(operation[6:])

    if operation not in cls.OPERATIONS:
      raise ValueError(f"Unsupported operation: {operation}")

    try:
      return cls.OPERATIONS[operation](*args)
    except TypeError:
      raise ValueError(f"Invalid number of arguments for operation: {operation}")
