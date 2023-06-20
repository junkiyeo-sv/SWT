# -*- coding: utf-8 -*-
"""gen_gtest.py tool sequence.

Execution path: root path
Execution parameters:  [Target hpp file path] [Save file path]

"""
import re, sys, os


class HppParser:
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __init__(self):
        ''' HppParser class constructor function
        
        1. Initialize variables used inside the HppParser class.
        
        Args:
            See comments below for object(self) variables
        '''
        # class_regex = class class_name(영문, 숫자, _,):
        class_regex = r"class\s+(?P<class_name>[a-zA-Z0-9_]+):*"
        # namespace_regex = namespace namespace_name(영문, 숫자, _)
        namespace_regex = r"namespace\s+(?P<namespace_name>[a-zA-Z0-9_]+)"
        # public_regex, non_public_regex (public :, public:)
        public_regex = r"public:|public\s:"
        non_public_regex = r"private:|private\s:|protected:|protected\s:"
        # function_regex = return_type(영문, 숫자, _, ::) function_name(영문, 숫자, _, ::) arguments(영문, 숫자, _)
        function_regex = r"(?P<return_type>[\w::&<>\s*]+)\s+(?P<function_name>[\w:]+)\((?P<arguments>.*)\)"
        # argument_regex = argument_type(영문, 숫자, _, *, &, const) argument_name(영문, 숫자, _)
        argument_regex = r"(?P<argument_type>.*(?:const\s+)?[\w\s*&]+)\s+(?P<argument_name>[\w]+)"
        
        # Regex pattern object variables (private)
        self.__class_pattern = re.compile(class_regex)
        self.__namespace_pattern = re.compile(namespace_regex)
        self.__public_pattern = re.compile(public_regex)
        self.__non_public_pattern = re.compile(non_public_regex)
        self.__function_pattern = re.compile(function_regex)
        self.__argument_pattern = re.compile(argument_regex)
        
        # Public variable
        self.class_map = {} # Data map of class in hpp code
        # Private variable
        self.__namespace_info = []  # Namespace data
        self.__current_class = ''   # Current class of line
        self.__previous_class = ''  # Previous class (for check nested class)
        self.__is_public = False    # Access specifier of line (public)
        self.__is_non_public = True # Access specifier of line (non public)
        self.__line_num = 0         # number of line
            
    # ---------------------------- function seperation line ------------------------------------ #
    def __find_namespaces(self, arg_line):
        ''' Find namespace in hpp code
        
        Args:
            arg_line: current line in hpp code
        '''
        # Find namespace (Regex match)
        namespace_match = self.__namespace_pattern.match(arg_line)
        if namespace_match:
            # Set namespace name
            self.__namespace_info.append(namespace_match.group('namespace_name'))
        
    # ---------------------------- function seperation line ------------------------------------ #
    def __find_classes(self, arg_line):
        ''' Find classes in hpp code
        
        Args:
            arg_line: current line in hpp code
        '''
        # Find class (Regex match)
        class_match = self.__class_pattern.match(arg_line)
        if class_match:
            
            # Find nested class (If the current_class exists, store it in the previous_class variable)
            if self.__current_class != '':
                self.__previous_class = self.__current_class
            
            # Set class name
            self.__current_class = class_match.group('class_name')
            self.__current_class = self.__current_class.strip()
            self.class_map[self.__current_class] = {}
            self.class_map[self.__current_class]['functions'] = []
            self.class_map[self.__current_class]['namespaces'] = []
            
            for name in self.__namespace_info:
                # Set namespace in class_map
                self.class_map[self.__current_class]['namespaces'].append(name)
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __find_nested_class(self, arg_line):
        ''' Find nested class in hpp code
        
        Args:
            arg_line: current line in hpp code
        '''
        # Find nested class (Find the endpoint of the previous_class)
        if "};" in arg_line and self.__previous_class != '':
            # Except for the case of "Type VariableName{ };" or If there are two as in "};};", the end point is correct
            if ("{" in arg_line and "};" in arg_line) == False or arg_line.count("};") == 2:
                self.__current_class = self.__previous_class
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __find_functions_argumnet(self, arg_line):
        ''' Find functions and function parameter in hpp code
        
        Args:
            arg_line: current line in hpp code
        '''
        # Find functions (Regex match)
        function_match = self.__function_pattern.match(arg_line)
        if function_match:
            # Set function return type, name, arguments
            function_return_type = function_match.group('return_type')
            function_name = function_match.group('function_name')
            function_arguments = function_match.group('arguments')
    
            argument_list = []
            arguments = function_arguments.strip().split(", ") # Arguments split
            for argument in arguments:
                # Find Arguments (Regex match)
                argument_match = self.__argument_pattern.match(argument)
                if argument_match:
                    # Set argument types and names
                    argument_type = argument_match.group('argument_type')
                    argument_name = argument_match.group('argument_name')
                    argument_list.append({"type": argument_type, "name": argument_name})
            
            # Construct a class map
            self.class_map[self.__current_class]["functions"].append({
                "return_type": function_return_type,
                "name": function_name,
                "arguments": argument_list
            })
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __chk_non_public(self, arg_line):
        ''' Check if the current line is public.
        
        Args:
            arg_line: current line in hpp code
        '''
        return_value = False
        # Parse only public functions
        public_match = self.__public_pattern.match(arg_line)
        non_public_match = self.__non_public_pattern.match(arg_line)
        if public_match:
            # In case of public method
            self.__is_public = True
            self.__is_non_public = False
        
        if non_public_match:
            # In case of private, protected method
            self.__is_public = False
            self.__is_non_public = True
        
        if self.__is_public is False and self.__is_non_public is True:
            return_value = True
        
        return return_value
    
    # ---------------------------- function seperation line ------------------------------------ #    
    def create_classes_map(self, target_hpp_path):
        ''' Create class and functions data in target hpp files
        
        1. Get one line from hpp file.
        2. Find namespace in hpp code
        3. Find classes. Also check for nested classes.
        4. Find public functions in a class. It also finds the function's parameters.
        
        Args:
            target_hpp_path: Target hpp path to create google test cpp file
        '''
        # Open hpp file
        f = open(target_hpp_path, 'r')
        lines = f.readlines()
        for line in lines:
            self.__line_num += 1
            line = line.lstrip() # Remove left blank in code
            line = line.rstrip() # Remove right blank in code
            
            if line == '' or line[:2] == '//':
                continue
            
            # Find namespace (Regex match)
            self.__find_namespaces(line)
            # Find nested class
            self.__find_nested_class(line)
            # Find class (Regex match)
            self.__find_classes(line)
            # Check private method
            if self.__chk_non_public(line):
                continue
            # Find functions and function parameters
            self.__find_functions_argumnet(line)
            
        print("\tEnd create_classes_map")
    

class GtestGenerator:

    # ---------------------------- function seperation line ------------------------------------ #
    def __init__(self):
        ''' GtestGenerator class constructor function
        
        1. Initialize variables used inside the GtestGenerator class.
        
        Args:
            See comments below for object(self) variables
        '''
        # Public variable
        self.gtest_code = ''        # Generated google test code
        # private variable
        self.__target_hpp_path = '' # Target hpp path to create google test cpp File
        self.__class_name = ''      # Class name
        self.__namespace_name = ''  # Namespace name
        self.__test_name = ''       # Test case name
        
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __create_test_head(self):
        ''' Create test code head.
        
        '''
        
        # Get file name 
        hpp_name = os.path.basename(self.__target_hpp_path)
        # Create test code head
        self.gtest_code = "\n".join([
                        "#include <iostream>", 
                        "",
                        "#include \"gtest/gtest.h\"", 
                        "#include \"testsuite_resources.h\"", 
                        "#include \"testcase_utils.hpp\"",
                        "", 
                        "#include \""+ hpp_name + "\"", 
                        "",
                        "/*",
                        "* This tool creates only \"Google Test\" form for functions of hpp files.",
                        "* Function parameters value and expected result value must be entered by the user.",
                        "*/",
                        "\n"
                        ])


    # ---------------------------- function seperation line ------------------------------------ #
    def __create_test_function(self, arg_test_body):
        ''' Create test function.
        
        Args:
            arg_test_body: Test body code data
        '''
        
        # Test information format comment
        test_info_form = \
                        "\t/*\n" \
                        "\t* TITLE: {}\n" \
                        "\t* DESC: {}\n" \
                        "\t* TEST_ENV: {}\n" \
                        "\t* TEST_METHOD: {}\n" \
                        "\t* TEST_CASE_GEN_METHOD: {}\n" \
                        "\t* RELATED_ID: {}\n" \
                        "\t* RISK_LEVEL: {}\n" \
                        "\t* ASIL: {}\n" \
                        "\t*/\n"

        # Create test information format
        test_info = test_info_form.format( \
                    self.__class_name + " " + self.__test_name, \
                    "Validate function \"" + self.__test_name + "\" of class \"" + self.__class_name + "\".", \
                    "", "", "", "", "", "" \
                )
        
        # Create test function code
        test_function = "\n".join([
                        "TEST(" + self.__class_name + ", " + self.__test_name + ")\n{",
                        test_info,
                        arg_test_body,
                        "}",
                        "\n"
                    ])
        
        return test_function


    # ---------------------------- function seperation line ------------------------------------ #
    def __create_test_body(self, arg_function_info):
        ''' Create test code body.

        Args: 
            arg_function_info: Data that stores function information
        '''
        
        # Check type when calling functions
        # Remove void type
        if arg_function_info["return_type"] == "void" or arg_function_info["return_type"] == "static void" or \
            arg_function_info["return_type"] == "virtual void":
            return_type_result = ""
            return_type_expected = ""
        # Remove static, virtual, inline type
        elif "static " == arg_function_info["return_type"][0:7]:
            return_type_result = arg_function_info["return_type"][7:] + " result_value = "
            return_type_expected = arg_function_info["return_type"][7:] + " expected_value;"
        elif "virtual " == arg_function_info["return_type"][0:8]:
            return_type_result = arg_function_info["return_type"][8:] + " result_value = "
            return_type_expected = arg_function_info["return_type"][8:] + " expected_value;"
        elif "inline " == arg_function_info["return_type"][0:7]:
            return_type_result = arg_function_info["return_type"][7:] + " result_value = "
            return_type_expected = arg_function_info["return_type"][7:] + " expected_value;"
        else:
            return_type_result = arg_function_info["return_type"] + " result_value = "
            return_type_expected = arg_function_info["return_type"] + " expected_value;"
        
        # Create input parameter    
        input_variable = "\n".join(["\t" + arg["type"] + " " + arg["name"] + ";" for arg in arg_function_info["arguments"]])
        
        # Generate the test case body
        test_body = "\n".join([
                    "\t// EXPECTED RESULT (You have to enter the value)",
                    "\t" + return_type_expected,
                    "\t// INPUT (You have to enter the value)",
                    input_variable,
                    "\t" + return_type_result + self.__namespace_name + "::"  + self.__class_name + "::" + \
                            arg_function_info["name"] + "(" + ", ".join([argument["name"] for argument in arg_function_info["arguments"]]) + ");",
                    "\t// EXPECT",
                    "\tEXPECT_EQ(result_value, expected_value);"
        ])
        
        return test_body
        

    # ---------------------------- function seperation line ------------------------------------ #
    def generate_gtest_cpp(self, arg_class_map, arg_target_hpp_path, arg_save_path):
        ''' Generate google test cpp file.
        
        Args: 
            arg_class_map: Data of classes and functions parsed at hpp file
            arg_target_hpp_path: Target hpp path to create google test cpp File
            arg_save_path: Google test cpp file storage path
        '''
        self.__target_hpp_path = arg_target_hpp_path
        # Create test code head
        self.__create_test_head()
        
        # Generate test cases for each class in the arg_class_map
        for class_name, class_info in arg_class_map.items():
            # Generate a test case for each public function in the class
            self.__class_name = class_name
            self.__namespace_name = "::".join(class_info['namespaces'])
            for function_info in class_info["functions"]:
                
                # Generate a test case name
                self.__test_name = function_info["name"] + "_test_001"
                
                # Create test code body
                test_body = self.__create_test_body(function_info)
                
                # Create test function
                test_function = self.__create_test_function(test_body)

                # Add the test case to the test code
                self.gtest_code += test_function
        
        # Create test cpp file
        f = open(arg_save_path, 'w')
        f.write(self.gtest_code)
        f.close
        
        print("\tEnd generate_gtest_cpp")


# ---------------------------- function seperation line ------------------------------------ #
if __name__ == "__main__":
    ''' main function
    
    Check the number of gen_gtest.py execution parameters and call the function.
    '''
    
    print("\033[94m" + "# RUN GOOGLE TEST CASE AUTOMATION GENERATION TOOL #\n" + "\033[0m")

    if len( sys.argv ) < 3:
        print("\033[31m" + "Python execution error: invalid execution parameter.\n" + "\033[0m")
        print("\033[92m" + "Python " + "%s [Target hpp file path] [Save file path]" % sys.argv[0] + "\033[0m")
        print("\033[92m" + "[Target hpp file path]\n"  + "\033[0m" + " - Ex. file_path/impl.hpp")
        print("\033[92m" + "[Save file path]\n"  + "\033[0m" + " - Ex. file_path/test_impl.cpp")
        exit()
    
    # Input parameters
    target_hpp_path = sys.argv[1]
    save_path = sys.argv[2]
    
    # Parsing hpp code
    hp = HppParser()
    hp.create_classes_map(target_hpp_path)
    # Generation test cpp file
    gg = GtestGenerator()
    gg.generate_gtest_cpp(hp.class_map, target_hpp_path, save_path)
    
    print("\033[94m" + "# END GOOGLE TEST CASE AUTOMATION GENERATION TOOL #\n" + "\033[0m")
    
