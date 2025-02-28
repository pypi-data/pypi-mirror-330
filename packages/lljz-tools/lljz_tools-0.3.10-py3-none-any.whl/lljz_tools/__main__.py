import sys
import argparse
from .pkg import main as _main


def main():
    parser = argparse.ArgumentParser(
        description="LLJZ Tools - 开发工具集",
        epilog="示例: lljz-tools pipreqs [output_file]"
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # pipreqs 命令
    pipreqs_parser = subparsers.add_parser(
        'pipreqs',
        help='生成requirements.txt文件',
        description='生成Python依赖文件')
    pipreqs_parser.add_argument(
        'output_file',
        nargs='?',
        default='requirements.txt',
        help='输出文件名（默认为requirements.txt）')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.command == 'pipreqs':
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(_main()))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
