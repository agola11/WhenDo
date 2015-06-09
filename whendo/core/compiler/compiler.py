"""
Description:

Author:
    Neil C

Usage:
    python [filename]

Python Version:
    2.7.5 

Notes:

"""
#==============================================================================
from time import sleep

class Compiler:

    def __init__(self, json_dict, setup_array, init_array):
        """
            json_dict:
                Must be a python dictionary object. The dictionary comes from
                the front-end visual programming interface
        """
        self.jsonDict = json_dict
        self.codeArray = []
        self.codeInitArray = []
        self.codeSetupArray = []
        self.setupArray = setup_array
        self.initArray = init_array

    def get_start(self):
        self.wPos = 1
        self.dPos = 1
        self.keyString = 'W1'
        self.codeArray.append('void loop()')
        self.codeArray.append('{')

    #TODO 
    def compiler_step(self):
        key_list = self.keyString.split('.')
        last_key = self.keyString.split('.')[-1]

        key_type = self.get_type(last_key)

        del key_list[-1]
        
        tier_string = '.'.join(key_list)

        if key_type == 'WHEN':
            self.prevKeyString = self.keyString
            next_key = self.get_compiler_step_when(tier_string, last_key)
            if tier_string == '':
                self.keyString = next_key
            else:
                self.keyString = tier_string + '.' + next_key
            return 'CONTINUE'

        elif key_type == 'DO':
            self.prevKeyString = self.keyString
            self.keyString = self.keyString + '.' + 'M'
            self.codeArray.append('{')
            return 'CONTINUE'
        
        elif key_type == 'MAIN_DO':
            self.prevKeyString = self.keyString
            next_key = self.get_compiler_step_m(tier_string)
            if next_key == 'DONE':
                return 'FINISHED'
            else:
                star_count = next_key.count('*')
                next_key = next_key.replace('*', '')
                if star_count == 0:
                    self.keyString = tier_string + '.' + next_key
                else:
                    for i in range(0, star_count):
                        _kl = tier_string.split('.')
                        del _kl[-1]
                        tier_string = '.'.join(_kl)

                    if tier_string == '':
                        self.keyString = next_key
                    else:
                        self.keyString = tier_string + '.' + next_key
                return 'CONTINUE'

                
            

    def get_compiler_step_m(self, tierString):
        options = self.get_val(tierString).keys()


        if 'W1' in options:
            return 'W1'
        else:
            steps_back = 1
            last_key = tierString.split('.')[-1]
            explore_tier = self.tier_step_back(tierString)
            previous_tier = explore_tier
            while True:
                if explore_tier == '':
                    options = self.jsonDict.keys()
                else:
                    options = self.get_val(explore_tier).keys() 
                next_w = 'W' + str(self.get_order(last_key) + 1)
                if next_w in options:
                    return '*' * steps_back + next_w
                else:
                    steps_back = steps_back + 1
                    last_key = explore_tier.split('.')[-1]
                    previous_tier = explore_tier
                    explore_tier = self.tier_step_back(explore_tier)
                    if explore_tier == '' and previous_tier == '':
                        break

            return 'DONE'


    def tier_step_back(self, tierString):
        key_list = tierString.split('.')
        del key_list[-1]
        return '.'.join(key_list)

    def get_compiler_step_when(self, tierString, key):
        if tierString == '':
            options = self.jsonDict.keys()
        else:
            options = self.get_val(tierString).keys()
            
        order = self.get_order(key)
        
        return 'D' + str(order)

            
        
         
    def get_order(self, key):
        """Gets the order of the key(i.e. W1 = 1)
        """
        order_val = key[1]
        try:
            v = int(order_val)
            return v
        except:
            return 0

    def get_type(self, key):
        if key[0] == 'W':
            return 'WHEN'
        elif key[0] == 'D':
            return 'DO'
        else:
            return 'MAIN_DO'
        

    #TODO
    def is_next(self):
        """ Determines if there is another line for the compiler to process
        """
        pass

    def get_val(self, tierString=None): 
        if tierString == None:
            dict_key_list = self.keyString.split('.')
        else:    
            dict_key_list = tierString.split('.')

        workingObj = self.jsonDict

        for compile_key in dict_key_list:
            workingObj = workingObj[compile_key]

        return workingObj

    def get_last_key(self):
        return self.keyString.split('.')[-1]

    def is_operator(self, val):
        if val == '&&' or val == '||' or val == '!':
            return True

    #TODO incorporate building of the lines
    def assemble(self, workingObj):
        #self.codeArray.append(self.keyString + ':')
        line_build = ''
        last_key = self.get_last_key()
        last_key_type = self.get_type(last_key)

        if last_key_type == 'WHEN':
            line_build += 'if ('
            if workingObj[0] == 1 or workingObj[0] == '1':
		line_build += '1)'
                self.codeArray.append(line_build)
                return
            if (workingObj[0] == '!'):
                line_build += '!'
                line_build += str(workingObj[1]) + '.'
            else:
                line_build += str(workingObj[0]) + '.'

            iter_pos = 0
            last_object_pos = 0
            last_operator_pos = -1
            for block_item in workingObj:
                if block_item == '!':
                    iter_pos += 1
                    continue

                if workingObj[iter_pos - 1] == '!':
                    iter_pos += 1
                    continue
                
                if block_item == workingObj[0]:
                    if block_item == '1':
                        line_build = line_build[:-1]
                        break
                

                else:
                    line_build += block_item
                    if self.is_operator(block_item):
                        line_build += ' '
                    elif not self.is_operator(workingObj[iter_pos - 1]):
                        line_build += '()'

                    if block_item != workingObj[-1]:
                        if self.is_operator(workingObj[iter_pos + 1]):
                            line_build += ' '
                        elif not self.is_operator(block_item):
                            line_build += '.'

                iter_pos += 1

            line_build += ')'
            self.codeArray.append(line_build)
        
        elif last_key_type == 'MAIN_DO':
            line_build += workingObj[0]
            if workingObj[0] == 'None':
                return 
            for block_item in workingObj:
                if block_item == workingObj[0]:
                    pass
                else:
                    line_build += '.' + block_item + '()'
            line_build += ';'
            self.codeArray.append(line_build)


        
        
    def insert_curly(self):
        last_key = self.get_last_key()

        if last_key[0] == 'W' and int(last_key[1]) > 1:
            #self.codeArray.append('}')
            key_string_diff = len(self.prevKeyString.split('.')) - len(self.keyString.split('.'))
            for i in range(0, key_string_diff):
                self.codeArray.append('}')


    def build(self, filename='block.pde'):
        self.get_start()

        self.build_init()
        self.build_setup()

        while True:
            cVal = self.get_val()

            self.assemble(cVal)
            
            cStep = self.compiler_step()
            
            self.insert_curly()


            if cStep == 'FINISHED':
                break

        in_count = self.codeArray.count('{')
        out_count = self.codeArray.count('}')
        diff_curly = in_count - out_count
        for i in range(0, diff_curly):
            self.codeArray.append('}')
        

        f = open(filename, 'w+')
        
        f.write('#include <Blockduino.h>\n')
        f.write('#include <Servo.h>\n')

        for line in self.codeInitArray:
            f.write(line)
            f.write('\n')
        
        f.write('void setup()')
        f.write('\n')
        f.write('{')
        f.write('\n')
        for line in self.codeSetupArray:
            f.write('    ')
            f.write(line)
            f.write('\n')
        f.write('}')
        f.write('\n')
        index_pos = 0 
        for line in self.codeArray:
            sub_array = self.codeArray[:index_pos]
            indent_level = sub_array.count('{') - sub_array.count('}')
            if line == '}':
                indent_level = indent_level - 1 
            out_line = ('    ' * indent_level) + line 
            f.write(out_line + '\n')
            index_pos = index_pos + 1


    def build_init(self):
        for block_line in self.initArray:
            line = block_line[0] + ' ' + block_line[1]
            if len(block_line) > 2:
                sub_array = block_line[2:]
                line += '('
                for sub in sub_array:
                    line += sub + ',' 
                line = line[:-1]
                line += ')'
            line += ';'
            self.codeInitArray.append(line)

    def build_setup(self):
        for block_line in self.setupArray:
            line = block_line[0] + '.' + block_line[1] + '('
            for block in block_line:
                if block == block_line[0] or block == block_line[1]:
                    pass
                else:
                    line += block + ','
            if line[-1] == ',':
                line = line[:-1]
            line += ');'
            self.codeSetupArray.append(line)



            


        

    
    
        
        

