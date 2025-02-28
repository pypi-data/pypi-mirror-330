import ast
from collections import OrderedDict
import os
import sys
from pathlib import Path

class OrderedDictExtractor(ast.NodeVisitor):
    def __init__(self):
        self.dicts = {}
        
    def visit_Assign(self, node):
        if (isinstance(node.value, ast.Call) and 
            isinstance(node.value.func, ast.Name) and 
            node.value.func.id == 'OrderedDict'):
            
            if len(node.value.args) == 1 and isinstance(node.value.args[0], ast.List):
                pairs = self._extract_pairs(node.value.args[0].elts)
                if hasattr(node.targets[0], 'id'):
                    self.dicts[node.targets[0].id] = OrderedDict(pairs)
    
    def _extract_pairs(self, elements):
        pairs = []
        for elt in elements:
            if isinstance(elt, ast.Tuple) and len(elt.elts) == 2:
                try:
                    key = self._extract_value(elt.elts[0])
                    value = self._extract_value(elt.elts[1])
                    pairs.append((key, value))
                except Exception as e:
                    print(f"Warning: Skipping pair due to error: {e}")
        return pairs
    
    def _extract_value(self, node):
        if isinstance(node, (ast.Constant, ast.Str)):
            return node.value if isinstance(node, ast.Constant) else node.s
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Tuple):
            return tuple(self._extract_value(elt) for elt in node.elts)
        elif isinstance(node, ast.IfExp):
            return self._extract_value(node.body)  # Take the true case as default
        return str(ast.unparse(node))

def process_file(input_file):
    """Process a single file and extract OrderedDict definitions"""
    input_path = Path(input_file)
    
    try:
        # Read and parse the file
        content = input_path.read_text(encoding='utf-8')
        tree = ast.parse(content)
        
        # Extract OrderedDict definitions
        extractor = OrderedDictExtractor()
        extractor.visit(tree)
        
        if not extractor.dicts:
            print(f"✅ No OrderedDict definitions found in {input_path.name}")
            return True
        
        # Create output file
        output_path = input_path.parent / f"extracted_{input_path.stem}.py"
        
        with output_path.open('w', encoding='utf-8') as f:
            f.write("from collections import OrderedDict\n\n")
            
            for name, ordered_dict in extractor.dicts.items():
                f.write(f"{name} = OrderedDict([\n")
                for key, value in ordered_dict.items():
                    f.write(f"    ({repr(key)}, {repr(value)}),\n")
                f.write("])\n\n")
        
        print(f"✅ Successfully processed {input_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {input_path.name}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python testing.py <input_file>")
        sys.exit(1)
        
    success = process_file(sys.argv[1])
    sys.exit(0 if success else 1)