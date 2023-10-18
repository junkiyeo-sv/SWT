# -*- coding: utf-8 -*-
"""repeat_test.py tool sequence.

Execution path: svnet dir
Execution parameters: python tool/repeat_test.py [Number of repeat test] [Test file name(accept multiple file)]
    [[Number of repeat test] ] Ex. 1 or 10
    [Test file name] Ex. test file name

Prepare. the latest branch, release mode build, run it from the svnet3 directory and root privileged account
1. Check for invalid parameter values in repeat_test.py.
2. Run test
3. Parsing your text
4. Create test data
"""
import os, sys, subprocess
from datetime import datetime


# ---------------------------- function seperation line ------------------------------------ #
if __name__ == "__main__":
    ''' main function
    
    Check the number of run_test.py execution parameters and call the function.
    '''    
    
    print("\033[94m" + "# RUN REPEAT TEST TOOL #\n" + "\033[0m")
    cwd = os.getcwd()
    run_wd = cwd.split('/')
    
    # Check invalid parameter
    if run_wd[len(run_wd)-1] != "#your root directory":
        print("\033[31m" + "Python execution error: python execution location must be run from the path." + "\033[0m")
        exit()
    elif len( sys.argv ) < 3: 
        print("\033[31m" + "Python execution error: invalid execution parameter." + "\033[0m")
        exit()
    
    test_iter_num = sys.argv[1]
    test_list = sys.argv[2].split(',')
    
    for test_name in test_list:
        # Create test file name
        current_year = str(datetime.today().year)
        file_name = "repeat_" + test_name + current_year[2:4] + datetime.today().strftime("%m%d" + "_" + "%H%M%S") + ".txt"
        result_txt = open(file_name, 'w')
        result_txt.close()
        
        os.chdir("build") # Move build dir
        expect_lines = []
        
        # Test data xml file parsing
        for idx in range(int(test_iter_num)):
            # Run test
            subprocess.call(['ctest', '-R', test_name])

            test_dir_path = "#your test file directory path (path after build directory) ex. test_dir/src/"
            
            # Open xml file
            try:
                result_xml = open(test_dir_path + test_name + ".xml", mode= 'r')
            except:
                expect_lines.append("Test run exception test: " + str(idx + 1) + ", " + test_name + "\n")
                continue

            expect_lines.append("Run test: " + str(idx + 1) + ", " + test_name + "\n")
            
            # Parsing test data in xml file
            for line in result_xml:
                if "<failure message=" in line :
                    expect_lines.append(line)

            result_xml.close()
            print("End test " + str(idx + 1) + ", " + test_name)
            # delete xml file
            subprocess.call(['rm', '-rf', test_dir_path + test_name + ".xml"])
        
        # Write test data
        result_txt = open(os.path.join(cwd, file_name), 'w')
        for line in expect_lines:
            #print(line)
            result_txt.write(line)
        result_txt.close()
        
        os.chdir(cwd)
        print("\n" + "\033[94m" + "# END REPEAT TEST TOOL #" + "\033[0m")
