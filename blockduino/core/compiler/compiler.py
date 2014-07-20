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

    def __init__(self, json_dict):
        """
            json_dict:
                Must be a python dictionary object. The dictionary comes from
                the front-end visual programming interface
        """
        self.jsonDict = json_dict

    def get_start(self):
        self.wPos = 1
        self.dPos = 1
        self.keyString = 'W1'

    #TODO 
    def compiler_step(self):
        print 'keyString: ', self.keyString
        key_list = self.keyString.split('.')
        last_key = self.keyString.split('.')[-1]

        key_type = self.get_type(last_key)

        del key_list[-1]
        
        tier_string = '.'.join(key_list)

        if key_type == 'WHEN':
            next_key = self.get_compiler_step_when(tier_string, last_key)
            if tier_string == '':
                self.keyString = next_key
            else:
                self.keyString = tier_string + '.' + next_key
            return 'CONTINUE'

        elif key_type == 'DO':
            self.keyString = self.keyString + '.' + 'M'
            return 'CONTINUE'
        
        elif key_type == 'MAIN_DO':
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
            while previous_tier != '' or explore_tier != '':
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

    #TODO incorporate building of the lines
    def assemble(self, workingObj):
        pass


    def build(self, filename='block.pde'):
        self.get_start()

        while True:
            cVal = self.get_val()

            self.assemble(cVal)
            
            cStep = self.compiler_step()

            sleep(1)

            if cStep == 'FINISHED':
                break



        

    
    
        
        

