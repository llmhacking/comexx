from ..tree_parser.custom_parser import CustomParser
from loguru import logger

class CParser(CustomParser):
    """Parser for C language"""

    def __init__(self, src_language, src_code):
        """Initialize the parser with the language."""
        super().__init__(src_language, src_code)

    def check_declaration(self, current_node):
        """Check if the node is a declaration."""
        # C declarations are typically variable or function declarations, no catch
        parent_types = ["parameter"]
        declaration_types = ['array_declarator', 'attributed_declarator', 'function_declarator', 'gnu_asm_expression', 'identifier', 'init_declarator', 'ms_call_modifier', 'parenthesized_declarator', 'pointer_declarator']
        parent_types.extend(declaration_types)
        
        current_types = ["identifier"]
        if (
                current_node.parent is not None
                and current_node.parent.type in parent_types
                and current_node.type in current_types
        ):
            return True
        return False
    
    def get_type(self, node):
        """ Given a variable declarator node, return the variable type of the identifier"""
        # https://github.com/tree-sitter/tree-sitter-c/blob/master/src/node-types.json -> "type": "type_specifier"
        datatypes = ['enum_specifier', 'macro_type_specifier', 'primitive_type', 'sized_type_specifier', 'struct_specifier', 'type_identifier', 'union_specifier']
        
        if node.type == "parameter_declaration":
            return node.children[0].text.decode('utf-8')

        for child in node.parent.children:
            if child.type in datatypes:
                return child.text.decode('utf-8')
        return None
    
    def scope_check(self, parent_scope, child_scope):
        """Check if the node is a scope."""
        for p in parent_scope:
            if p not in child_scope:
                return False
        return True
    
    def longest_scope_match(self, name_matches, symbol_table):
        """Given a list of name matches, return the longest scope match"""
        # [(ind, var), (ind,var)]
        scope_array = list(map(lambda x: symbol_table['scope_map'][x[0]], name_matches))
        # scope_array.sort(key=lambda x: len(x), reverse=True)
        # index = max(range(len(scope_array)), key=lambda x: len(x))
        max_val = max(scope_array, key=lambda x: len(x))
        for i in range(len(scope_array)):
            if scope_array[i] == max_val:
                return name_matches[i][0]
            
    def create_all_tokens(
        self,
        src_code,
        root_node,
        all_tokens,
        label,
        method_map,
        method_calls,
        start_line,
        declaration,
        declaration_map,
        symbol_table,
    ):
        remove_list = [
            "struct_specifier",
            "function_definition",
            "call_expression",
            # 'constructor_initializer', 'implicit_object_creation_expression', 'object_creation_expression', 'primary_constructor_base_type'
        ]
        block_types = [
            "block",
            "if_statement",
            "while_statement",
            "for_statement",
            "compound_statement",
            "do_statement",
            "switch_statement",
            "seh_try_statement",
            "seh_leave_statement",
            
            "function_definition",
        ]

        if root_node.is_named and root_node.type in block_types:
            # print(root_node.type)
            # current_scope = symbol_table['scope_stack'][-1]
            symbol_table["scope_id"] = symbol_table["scope_id"] + 1
            symbol_table["scope_stack"].append(symbol_table["scope_id"])

        if (
                root_node.is_named
                and (len(root_node.children) == 0 or root_node.type == "string")
                and root_node.type != "comment"
        ):
            index = self.index[
                (root_node.start_point, root_node.end_point, root_node.type)
            ]
            label[index] = root_node.text.decode("UTF-8")
            # if label[index] == 'true':
            #     print("FOUND TRUEE")
            start_line[index] = root_node.start_point[0]
            all_tokens.append(index)
            symbol_table["scope_map"][index] = symbol_table["scope_stack"].copy()
            # print("Adding to scope map", index, symbol_table['scope_map'][index])

            current_node = root_node

            if (
                    current_node.parent is not None
                    and current_node.parent.type in remove_list
            ):
                method_map.append(index)
                # print(current_node.text.decode('utf-8'), current_node.next_named_sibling)
                if (
                    current_node.next_named_sibling is not None and
                    current_node.next_named_sibling.type == "argument_list"
                ):
                    # print("ADDING METHOD", current_node.type, current_node.text.decode('utf-8'))
                    method_calls.append(index)

            if (
                    current_node.parent is not None
                    and current_node.parent.type == "field_expression"
            ):
                # field_expression [13, 34] - [13, 45]
                #   argument: identifier [13, 34] - [13, 40]
                #   field: field_identifier [13, 41] - [13, 45]
                object_node = current_node.parent.child_by_field_name("field")
                object_index = self.index[
                    (object_node.start_point, object_node.end_point, object_node.type)
                ]
                current_index = self.index[
                    (
                        current_node.start_point,
                        current_node.end_point,
                        current_node.type,
                    )
                ]
                if object_index == current_index:
                    # ? not sure about this yet Console.writeline - if i say expression it will pick console if i say name it will pick the object but java side it picks the parent?
                    method_map.append(current_index)

                while (
                        current_node.parent is not None
                        and current_node.parent.type == "field_expression"
                ):
                    if current_node.parent.next_named_sibling is not None and current_node.parent.next_named_sibling.type == "argument_list":
                        break
                    else:
                        current_node = current_node.parent

                if (
                        current_node.parent is not None
                        and current_node.parent.type == "call_expression"
                ):
                    method_map.append(index)
                label[index] = current_node.text.decode("UTF-8")

            if self.check_declaration(current_node):
                variable_name = label[index]
                declaration[index] = variable_name

                variable_type = self.get_type(current_node.parent)
                if variable_type is not None:
                    symbol_table["data_type"][index] = variable_type
            else:
                current_scope = symbol_table['scope_map'][index]
                if current_node.type == "field_expression":
                    field_variable = current_node.children[-1]
                    # entire_variable_name = current_node.text.decode('utf-8')
                    field_variable_name = field_variable.text.decode('utf-8')
                    
                    for (ind,var) in declaration.items():
                        if var == field_variable_name:
                            parent_scope = symbol_table['scope_map'][ind]
                            if self.scope_check(parent_scope, current_scope):
                                declaration_map[index] = ind
                                break
                else:
                    name_matches = []
                    for (ind, var) in declaration.items():
                        if var == label[index]:
                            parent_scope = symbol_table['scope_map'][ind]
                            if self.scope_check(parent_scope, current_scope):
                                name_matches.append((ind,var))
                    for (ind, var) in name_matches:
                        parent_scope = symbol_table['scope_map'][ind]
                        closest_index = self.longest_scope_match(name_matches, symbol_table)
                        declaration_map[index] = closest_index
                        break

        else:
            for child in root_node.children:
                self.create_all_tokens(
                    src_code,
                    child,
                    all_tokens,
                    label,
                    method_map,
                    method_calls,
                    start_line,
                    declaration,
                    declaration_map,
                    symbol_table,
                )

        if root_node.is_named and root_node.type in block_types:
            symbol_table["scope_stack"].pop(-1)

        return (
            all_tokens,
            label,
            method_map,
            method_calls,
            start_line,
            declaration,
            declaration_map,
            symbol_table,
        )
    
    