import ast
def sparta_e867fa639f(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_17a52f649e(script_text):return sparta_e867fa639f(script_text)