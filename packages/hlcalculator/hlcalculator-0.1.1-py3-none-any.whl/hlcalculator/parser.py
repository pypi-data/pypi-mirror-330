"""
命令行参数解析器

主要功能:
1. 解析命令行参数，支持两种命令模式：
   - calc: 执行计算操作
   - const: 获取数学常数值
2. 提供详细的使用说明和示例
3. 支持多种运算格式：
   - 基础运算：python main.py calc 5 + 3
   - 科学运算：python main.py calc 16 sqrt
   - 常数查询：python main.py const pi

使用示例:
    # 基础运算
    python main.py calc 5 + 3        # 输出: 8.0
    python main.py calc 2 '*' 3      # 输出: 6.0 (注意：乘号需要引号)

    # 科学运算
    python main.py calc 16 sqrt      # 输出: 4.0
    python main.py calc 5 factorial  # 输出: 120.0

    # 获取常数
    python main.py const pi          # 输出: 3.141592653589793
"""
import argparse
from typing import Tuple, List, Union
from decimal import Decimal, InvalidOperation


def create_parser() -> argparse.ArgumentParser:
  """创建并配置命令行参数解析器

  配置包括:
  1. 设置程序描述和帮助信息
  2. 创建子命令解析器（calc和const）
  3. 配置每个子命令的参数
  4. 添加使用示例

  返回:
      配置好的ArgumentParser实例

  使用示例:
      parser = create_parser()
      args = parser.parse_args()
      # args.command 将是 'calc' 或 'const'
      # 对于calc命令，args.expression 将包含要计算的表达式
      # 对于const命令，args.name 将包含常数名称
  """
  parser = argparse.ArgumentParser(
    description="HLCalculator - An advanced command line calculator",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  Basic Operations:
    %(prog)s calc 5 + 3        # Addition: 8.0
    %(prog)s calc 10 - 4       # Subtraction: 6.0
    %(prog)s calc 3 '*' 4      # Multiplication: 12.0
    %(prog)s calc 15 / 3       # Division: 5.0
    %(prog)s calc 2 ^ 3        # Power: 8.0

  Scientific Operations:
    %(prog)s calc 16 sqrt      # Square root: 4.0
    %(prog)s calc 100 log 10   # Log base 10: 2.0
    %(prog)s calc 0.5 sin      # Sine (in radians): 0.479
    %(prog)s calc 5 factorial  # Factorial: 120.0

  Constants:
    %(prog)s const pi          # π: 3.141592653589793
    %(prog)s const e           # e: 2.718281828459045

Note: For multiplication, enclose '*' in quotes to prevent shell expansion.
"""
  )

  subparsers = parser.add_subparsers(dest='command', help='Command to execute')

  # Calculator command
  calc_parser = subparsers.add_parser('calc', help='Perform a calculation')
  calc_parser.add_argument('expression', nargs='+', help='Expression to evaluate')

  # Constant command
  const_parser = subparsers.add_parser('const', help='Get mathematical constant')
  const_parser.add_argument('name', choices=['pi', 'e', 'tau'], help='Constant name')

  return parser


def parse_calculation(args: List[str]) -> Tuple[str, List[Union[int, float, Decimal]]]:
  """解析计算表达式参数

  将输入的计算表达式解析为操作符和操作数。支持两种格式：
  1. 双目运算：[数字1] [运算符] [数字2]
     例如：5 + 3、10 '*' 2
  2. 单目运算：[数字] [运算符]
     例如：16 sqrt、5 factorial

  参数:
      args: 包含计算表达式的字符串列表

  返回:
      (operation, operands) 元组，其中:
      - operation: 运算符字符串
      - operands: 操作数列表

  异常:
      ValueError: 当参数格式不正确或数字无效时抛出

  示例:
      # 双目运算
      parse_calculation(['5', '+', '3']) -> ('+', [Decimal('5'), Decimal('3')])

      # 单目运算
      parse_calculation(['16', 'sqrt']) -> ('sqrt', [Decimal('16')])
  """
  if len(args) < 2:
    raise ValueError("Not enough arguments for calculation")

  # Handle scientific operations
  scientific_ops = {'sqrt', 'sin', 'cos', 'tan', 'factorial'}
  if args[-1] in scientific_ops:
    if len(args) != 2:
      raise ValueError(f"{args[-1]} operation takes exactly one argument")
    try:
      return args[-1], [Decimal(args[0])]
    except InvalidOperation:
      raise ValueError(f"Invalid number: {args[0]}")

  # Handle binary operations
  if len(args) != 3:
    raise ValueError("Binary operations require exactly two numbers")

  try:
    x = Decimal(args[0])
    y = Decimal(args[2])
  except InvalidOperation as e:
    raise ValueError(f"Invalid number in expression: {e}")

  operation = args[1]

  return operation, [x, y]


def parse_arguments():
  """解析命令行参数

  解析并验证用户输入的命令行参数，支持以下功能：
  1. 如果没有提供命令，显示帮助信息
  2. 对于calc命令，解析计算表达式
  3. 对于const命令，返回常数查询格式

  返回:
      对于calc命令：(operation, operands)
      对于const命令：('const:name', [])
      显示帮助信息时：None

  异常:
      ValueError: 当命令无效或参数格式错误时抛出

  使用示例:
      # 计算 5 + 3
      python main.py calc 5 + 3
      # 结果: ('+', [Decimal('5'), Decimal('3')])

      # 获取 π 值
      python main.py const pi
      # 结果: ('const:pi', [])
  """
  parser = create_parser()
  args = parser.parse_args()

  if not args.command:
    parser.print_help()
    return None

  if args.command == 'const':
    return f'const:{args.name}', []

  if args.command == 'calc':
    return parse_calculation(args.expression)

  raise ValueError(f"Unknown command: {args.command}")
