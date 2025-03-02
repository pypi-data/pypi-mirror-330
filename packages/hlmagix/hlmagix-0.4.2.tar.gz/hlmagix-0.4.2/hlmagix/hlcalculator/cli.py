#!/usr/bin/env python
"""
HLCalculator CLI implementation module.
Contains the main CLI functionality and result formatting.
"""
import sys
from decimal import InvalidOperation

from hlmagix.hlcalculator import parse_arguments, ScientificCalculator


def format_result(result: float) -> str:
  """格式化计算结果

  根据数值大小自动选择合适的显示格式：
  1. 大数和小数使用科学计数法
  2. 整数结果显示一位小数
  3. 小数结果去除尾部多余的0

  参数:
      result: 要格式化的计算结果

  返回:
      格式化后的字符串

  示例:
      format_result(1000000)    -> "1.000000e+06"
      format_result(5)          -> "5.0"
      format_result(3.14159)    -> "3.14159"
  """
  # For large or small numbers, use scientific notation
  abs_result = abs(result)
  if abs_result > 1e6 or (abs_result < 1e-6 and abs_result != 0):
    return f"{result:.6e}"

  # For regular numbers, use standard decimal format
  if result.is_integer():
    return f"{result:.1f}"
  return f"{result:.6f}".rstrip('0').rstrip('.')


def main() -> None:
  """计算器主程序入口

  主要流程:
  1. 解析命令行参数
  2. 执行计算操作
  3. 格式化并输出结果

  异常处理:
  - ValueError: 参数错误、计算错误等
  - InvalidOperation: 数值格式错误
  - 其他未预期的异常

  退出码:
  - 0: 正常退出
  - 1: 发生错误
  """
  try:
    # Parse arguments
    result = parse_arguments()
    if result is None:  # Help was displayed
      return

    operation, args = result

    # Perform calculation
    try:
      result = ScientificCalculator.calculate(operation, *args)
      print(format_result(result))
    except (ValueError, InvalidOperation) as e:
      print(f"Error: {str(e)}", file=sys.stderr)
      sys.exit(1)

  except Exception as e:
    print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
  main()
