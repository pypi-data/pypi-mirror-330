import os
import sys
import argparse


def accept(line: str, tool: str, filters: list):
    if 'ok' not in line:
        return False
    if tool not in line:
        return False
    for f in filters:
        if f not in line:
            return False
    return True


def run(file: str, tool: str, filter:list):
    if not os.path.exists(file):
        print("ERROR: file not found")
        return
    with open(file) as f:
        lines = f.read().splitlines(keepends=False)

    # print(f"Loaded {len(lines)} lines")
    # for line in lines:
    #     print(line)
    print("Filters are")
    for f in filter:
        print(f)
    data = [ line for line in lines if accept(line, tool, filter)]
    runtime = 0
    memory = 0
    count = 0
    for line in data:
        parts = line.split('|')
        if parts[3].strip() == 'ok':
            print(line)
            runtime += float(parts[-2])
            memory += float(parts[-3])
            count += 1
        else:
            print(f"Rejecting line {parts[3]}: {line}")
    if count == 0:
        print("ERROR: No lines matched the given query")
        return

    print(f"{memory/count:3.3f}GB {runtime/count:5.2f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs=1)
    parser.add_argument('-t', '--tool', help='Tool name to filter on')
    parser.add_argument('-f', '--filter', help='A string to also filter on', nargs='+')
    args = parser.parse_args(sys.argv[1:])
    run(args.file[0], args.tool, args.filter)
