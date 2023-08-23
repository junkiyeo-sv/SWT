# -*- coding: utf-8 -*-
"""Testcase addition and modification tool using codebeamer_api.py tool

The CodeBeamerAPI class is a library implemented to request get, post, 
    put, and delete data from the server using the codebeamer Rest API.

See function comment out for further explanation.
"""
import codebeamer_api, re, time, sys

class GtestParser:
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __init__(self):
        ''' GtestParser class constructor function
        
        Args: none
        
        Ret: none
        '''
        self.line_num = 0
        self.testcase_info_map = {}
    
    # ---------------------------- function seperation line ------------------------------------ #
    def create_testcases_map(self, test_file_path):
        ''' Generate test case information map by parsing google test source code
        
        Args: 
            test_file_path: google test source code file path
        
        Ret: 
            testcase_info_map: test case information map
        '''
        f = open(test_file_path, 'r')
        lines = f.readlines()
        gtest_func_patter = r'\((.*?)\)'
        test_info_pattern = r'\*\s*(\w+):\s*(.+)'
        current_testcase = ''
        
        for line in lines:
            self.line_num += 1
            line = line.lstrip() # Remove left blank in code
            line = line.rstrip() # Remove right blank in code
            
            # Parse only the necessary lines
            if not(line[:5] == 'TEST(' or line[:7] == 'TEST_F(' or line[:2] == '//' or \
                line[:2] == '/*' or line[:1] == '*' or line[:2] == '*/'):
                continue
            
            # Parsing the TEST or TEST_F function name
            if 'TEST(' in line or 'TEST_F(' in line:
                gtest_func_match = re.findall(gtest_func_patter, line)
                func_name = gtest_func_match[0]
                func_name = func_name.replace(' ', '').replace(',','_')
                self.testcase_info_map[func_name] = {}
                current_testcase = func_name
                continue
            
            # Parsing the test case TITLE
            if '* TITLE' in line:
                title_match = re.match(test_info_pattern, line)
                title_key = 'TITLE'
                title_value = 'TITLE is empty'
                if title_match is not None:
                    title_key = title_match.group(1)
                    title_value = title_match.group(2)
                self.testcase_info_map[current_testcase][title_key] = title_value
                continue
            
            # Parsing the test case DESC
            if '* DESC' in line:
                desc_match = re.match(test_info_pattern, line)
                desc_key = 'DESC'
                desc_value = 'DESC is empty'
                if desc_match is not None:
                    desc_key = desc_match.group(1)
                    desc_value = desc_match.group(2)
                self.testcase_info_map[current_testcase][desc_key] = desc_value
                continue
            
            # Parsing the test case TEST_ENV
            if '* TEST_ENV' in line:
                test_env_match = re.match(test_info_pattern, line)
                test_env_key = 'TEST_ENV'
                test_env_value = 'TEST_ENV is empty'
                if test_env_match is not None:
                    test_env_key = test_env_match.group(1)
                    test_env_value = test_env_match.group(2)
                self.testcase_info_map[current_testcase][test_env_key] = test_env_value
                continue
            
            # Parsing the test case TEST_METHOD
            if '* TEST_METHOD' in line:
                test_method_match = re.match(test_info_pattern, line)
                test_method_key = 'TEST_METHOD'
                test_method_value = 'TEST_METHOD is empty'
                if test_method_match is not None:
                    test_method_key = test_method_match.group(1)
                    test_method_value = test_method_match.group(2)
                self.testcase_info_map[current_testcase][test_method_key] = test_method_value
                continue
            
            # Parsing the test case TEST_CASE_GEN_METHOD
            if '* TEST_CASE_GEN_METHOD' in line:
                test_case_gen_method_match = re.match(test_info_pattern, line)
                test_case_gen_method_key = 'TEST_CASE_GEN_METHOD'
                test_case_gen_method_value = 'TEST_CASE_GEN_METHOD is empty'
                if test_case_gen_method_match is not None:
                    test_case_gen_method_key = test_case_gen_method_match.group(1)
                    test_case_gen_method_value = test_case_gen_method_match.group(2)
                self.testcase_info_map[current_testcase][test_case_gen_method_key] = test_case_gen_method_value
                continue
            
            # Parsing the test case RELATED_ID
            if '* RELATED_ID' in line:
                related_id_match = re.match(test_info_pattern, line)
                related_id_key = 'RELATED_ID'
                related_id_value = 'RELATED_ID is empty'
                if related_id_match is not None:
                    related_id_key = related_id_match.group(1)
                    related_id_value = related_id_match.group(2)
                self.testcase_info_map[current_testcase][related_id_key] = related_id_value
                continue
            
            # Parsing the test case RISK_LEVEL
            if '* RISK_LEVEL' in line:
                risk_level_match = re.match(test_info_pattern, line)
                risk_level_key = 'RISK_LEVEL'
                risk_level_value = 'RISK_LEVEL is empty'
                if risk_level_match is not None:
                    risk_level_key = risk_level_match.group(1)
                    risk_level_value = risk_level_match.group(2)
                self.testcase_info_map[current_testcase][risk_level_key] = risk_level_value
                continue
            
            # Parsing the test case ASIL
            if '* ASIL' in line:
                asil_match = re.match(test_info_pattern, line)
                asil_key = 'ASIL'
                asil_value = 'ASIL is empty'
                if asil_match is not None:
                    asil_key = asil_match.group(1)
                    asil_value = asil_match.group(2)
                self.testcase_info_map[current_testcase][asil_key] = asil_value
                continue
        
        print("completed testcase info parsing")
        return self.testcase_info_map


class CodeBeamerTestcaseManager:
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __init__(self, id, pwd):
        ''' Codebeamer session connection constructor
        
        Args: 
            id: codebeamer user id (rest api permission required)
            pwd: codebeamer user password
        
        Ret: none
        '''
        self.cb = codebeamer_api.CodeBeamerAPI()
        response = self.cb.request_session('your codebeamer REST API uri', id, pwd)
        self.__check_status_code(response)
    
    # ---------------------------- function seperation line ------------------------------------ #
    def __check_status_code(self, response):
        ''' Response verification for codebeamer_api function
        
        Args: 
            response: codebeamer_api function return value
        
        Ret: 
            ret_value: response value or tool terminate after print error message
        '''
        if response[0] == 200:
            return response[1]
        else:
            print('\033[31m' + response[1] + '\033[0m')
            exit()
    
    # ---------------------------- function seperation line ------------------------------------ #
    def add_testcases(self, project_name, tracker_name, tc_info):
        ''' Add testcases to codebeamer server using testcase_info_map
        
        Args: 
            project_name: codebeamer projcet name
            tracker_name: tracker/category name to add test case
            tc_info: testcase_info_map generated by the create_testcases_map function
        
        Ret: none
        '''
        response = self.cb.get_project_uri(project_name)
        project_uri = self.__check_status_code(response)
        
        # Get command delay (if no sleep, it is not updated)
        time.sleep(0.5)

        response = self.cb.get_category_uri(project_uri, tracker_name)
        category_uri = self.__check_status_code(response)
        
        item_headers = {'Content-Type': 'application/json'}
        item_body = {
            "name"        : "",
            "tracker"     : "",
            "status"      : "",
            "type"        : "",
            "description" : "",
            "priority"    : "",
            "reusable"    : False
        }
        for tc in tc_info:
            # Post command delay (if no sleep, it is not updated)
            time.sleep(0.7)
            
            item_body['name'] = tc_info[tc]['TITLE']
            item_body['tracker'] = project_uri + category_uri
            item_body['status'] = 'New'
            item_body['type'] = 'Functional'
            item_body['description'] = tc_info[tc]['DESC']
            item_body['priority'] = 'Normal'
            
            response = self.cb.post_item(item_headers, item_body)
            if response[0] == 201:
                print('\033[32m' + response[1] + '\033[0m' + ', '+ tc_info[tc]['TITLE'])
            else:
                print('\033[31m' + response[1] + '\033[0m' + ', '+ tc_info[tc]['TITLE'])
        
        print("added test case information done")

    # ---------------------------- function seperation line ------------------------------------ #
    def update_testcases(self, project_name, tracker_name, tc_info):
        ''' Update testcases to codebeamer server using testcase_info_map
        
        Args: 
            project_name: codebeamer projcet name
            tracker_name: tracker/category name to update test case
            tc_info: testcase_info_map generated by the create_testcases_map function
        
        Ret: none
        '''
        response = self.cb.get_project_uri(project_name)
        project_uri = self.__check_status_code(response)
        
        # Get command delay (if no sleep, it is not updated)
        time.sleep(0.5)

        response = self.cb.get_category_uri(project_uri, tracker_name)
        category_uri = self.__check_status_code(response)
        
        # Get command delay (if no sleep, it is not updated)
        time.sleep(0.5)
        
        item_headers = {'Content-Type': 'application/json'}
        item_body = {
            "uri"         : "", 
            "description" : "", 
            "type"        : "", 
            "priority"    : ""
        }
        
        for tc in tc_info:
            # Post command delay (if no sleep, it is not updated)
            time.sleep(0.7)
            
            response = self.cb.get_item_uri(project_uri, category_uri, tc_info[tc]['TITLE'])
            item_uri = self.__check_status_code(response)
            
            # Get command delay (if no sleep, it is not updated)
            time.sleep(0.5)
            
            item_body['uri'] = item_uri
            item_body['type'] = 'Functional'
            item_body['description'] = tc_info[tc]['DESC']
            item_body['priority'] = 'Normal'
            
            response = self.cb.put_item(item_headers, item_body)
            if response[0] == 200:
                print('\033[32m' + response[1] + '\033[0m' + ', '+ tc_info[tc]['TITLE'])
            else:
                print('\033[31m' + response[1] + '\033[0m' + ', '+ tc_info[tc]['TITLE'])
        
        print("added test case information done")
        
    # ---------------------------- function seperation line ------------------------------------ #
    def delete_testcases(self):
        ''' Delete testcases to codebeamer server
            codebeamer_api에서 delete API는 개발완료되었으나, 삭제 로직에 대해서는 추후 추가 예정
        Args: 
                    
        Ret: none
        '''
        print()

# ---------------------------- function seperation line ------------------------------------ #
if __name__ == "__main__":
    ''' main function 
    '''
    if len(sys.argv) < 7:
        print("\033[31m" + "Python execution error: invalid execution parameter.\n" + "\033[0m")
        print("\033[92m" + "Python " + "%s [testcase_path] [id] [pwd] [project_name] [tracker_name] [testcase_mode]" % sys.argv[0] + "\033[0m")
        print("\033[92m" + "[testcase_path]\n"  + "\033[0m" + " - Ex. file_path/tc.cpp")
        print("\033[92m" + "[id]\n"  + "\033[0m" + " - Ex. codebeamer account id")
        print("\033[92m" + "[pwd]\n"  + "\033[0m" + " - Ex. codebeamer account password")
        print("\033[92m" + "[project_name]\n"  + "\033[0m" + " - Ex. codebeamer project name")
        print("\033[92m" + "[tracker_name]\n"  + "\033[0m" + " - Ex. codebeamer tracker/category name")
        print("\033[92m" + "[testcase_mode]\n"  + "\033[0m" + " - Ex. add testcase = 0, update testcase = 1")
        exit()
        
    testcase_path = sys.argv[1]
    cb_id = sys.argv[2]
    cb_pwd = sys.argv[3]
    project_name = sys.argv[4]
    tracker_name = sys.argv[5]
    testcase_mode = int(sys.argv[6])
    print(testcase_mode)
    if not(testcase_mode == 0 or testcase_mode == 1):
        print("\033[92m" + "[testcase_mode]\n"  + "\033[0m" + " - Ex. add testcase = 0, update testcase = 1")
        exit()
    
    gp = GtestParser()
    testcase_info = gp.create_testcases_map(testcase_path)
    
    cbtm = CodeBeamerTestcaseManager(cb_id, cb_pwd)
    if testcase_mode == 0:
        cbtm.add_testcases(project_name, tracker_name, testcase_info)
    elif testcase_mode == 1:
        cbtm.update_testcases(project_name, tracker_name, testcase_info)
    
