__author__ = 'Girish'
import subprocess
import os
import re
import sys
#todo - use a better method then the subprocess to run the script
import time
class InvalidFileException(Exception):
    def __init__(self, statement=None):
        if statement:
            Exception.__init__(self, statement)
        else:
            Exception.__init__(self)


class Compiler:
    permissive_regex = re.compile("\.{2}")
    def __init__(self, exec_command, file=None):
        if file:
            self.solution = file
        self.exec_command = exec_command

    def set_solution_file(self, file):
        self.solution = file

    def _prepare_compilation_statement(self, file, *args, **kargs):
        if self.permissive_regex.search(file):
            raise InvalidFileException("The file is trying to access another folder.")
        statement = [self.exec_command, file]
        for key, val in kargs.items():
            if len(key) == 1:
                statement.append("-" + key)
            else:
                statement.append("--" + key)
            statement.append(val)
        return " ".join(statement)

    def _format_input(self, input_tuple):
        out = input_tuple[0].decode()
        out = out.splitlines()
        return out

    def _get_Test_output(self, file,test, *args, **kargs):
        statement = self._prepare_compilation_statement(file, *args, **kargs)
        infile = subprocess.Popen(statement, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if not os.path.isfile(test):
            raise InvalidFileException("the test file not found")
            infile.kill()
        with open(test) as testfile:
            t=time.time()
            out = infile.communicate(input="".join(testfile.readlines()).encode())
            self.time=time.time()-t
            return self._format_input(out)

    def TestCase(self,file,test,checkfile,limit,*args,**kwargs):
        out =self._get_Test_output(file,test,*args,**kwargs)
        if limit >self.time:
            return "Time limit Exceed"
        return self.check_result_against_out(checkfile,out)

    def check_result_against_out(self,check, out_tuple):
        try:
            with open(check) as outfile:
                counter = 1
                bo = True
                for word in outfile.readlines():
                    word = word.strip()
                    if word != out_tuple[counter - 1]:
                        print("OUTPUT fails at {} \n \t EXPECTED : {} \t GOT: {} \n\n".format(counter, word,
                                                                                              out_tuple[counter - 1]))
                        bo = False
                    counter += 1
                return "Test Case Passed" if bo else "Test Case Failed"
        except FileNotFoundError:
            print("the output file not found")
        except IndexError:
            print("the script provided has compilation errors")
