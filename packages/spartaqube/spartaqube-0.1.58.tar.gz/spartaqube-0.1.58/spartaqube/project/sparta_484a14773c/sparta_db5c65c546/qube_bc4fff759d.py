import ast
def sparta_6d42611b5c(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_97dc1a947f(script_text):return sparta_6d42611b5c(script_text)