import argparse
import os

from executor import Executor
from tokeniser import Tokeniser
from parser import Parser
from transpiler import Transpiler

def is_old_file(filename):
	return filename.endswith('.old')

def run_old_file(filepath):
	with open(filepath, 'r') as f:
		code = f.read()
	tokens = Tokeniser.tokenise(code)
	ast = Parser.parse(tokens)
	exe = Executor()
	exe.execute(ast)


def main():
	parser = argparse.ArgumentParser(description='OldLang CLI')
	subparsers = parser.add_subparsers(dest='command', required=True)

	run_parser = subparsers.add_parser('run', help='Run an OldLang .old file')
	run_parser.add_argument('file', help='Path to a .old file to run')

	transpile_parser = subparsers.add_parser('transpile', help='Transpile OldLang .old file to Python')
	transpile_parser.add_argument('input', help='Path to a .old file to transpile')
	transpile_parser.add_argument('output', help='Path to output Python file')

	list_parser = subparsers.add_parser('list', help='List all .old files in the current directory')

	args = parser.parse_args()

	if args.command == 'list':
		files = [f for f in os.listdir('.') if is_old_file(f)]
		if files:
			print('Found .old files:')
			for f in files:
				print(f)
		else:
			print('No .old files found.')
		return

	if args.command == 'run':
		if not is_old_file(args.file):
			print('Error: File must have a .old extension')
			return
		if not os.path.exists(args.file):
			print(f'Error: File {args.file} does not exist')
			return
		with open(args.file, 'r') as f:
			code = f.read()
		tokens = Tokeniser.tokenise(code)
		ast = Parser.parse(tokens)
		exe = Executor()
		exe.execute(ast)
		return

	if args.command == 'transpile':
		if not is_old_file(args.input):
			print('Error: Input file must have a .old extension')
			return
		if not os.path.exists(args.input):
			print(f'Error: File {args.input} does not exist')
			return
		with open(args.input, 'r') as f:
			code = f.read()
		tokens = Tokeniser.tokenise(code)
		ast = Parser.parse(tokens)
		py_code = Transpiler.transpile(ast)
		with open(args.output, 'w') as outf:
			outf.write(py_code)
		print(f'Transpiled {args.input} to {args.output}')
		return

if __name__ == '__main__':
	main()
