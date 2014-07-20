from compiler import Compiler
d1 = {'W1': 't in W1', 'D1' : {'M' : 't in D1.M', 'W1' : 't in D1.W1', 'D1' : {'M' : 't in D1.D1.M'}, 'W2' : 't in D1.W2', 'D2': {'M': 't in D1.D2.M', 'W1': 't in D1.D2.W1', 'D1' : {'M': 't in D1.D2.D1.M'}, 'W2' : 't in D1.D2.W2', 'D2' : {'M': 't in D1.D2.D2.M'}, 'W3' : 't in D1.D2.W3', 'D3' : {'M' : 't in D1.D2.D3.M'}}, 'W3': 't in D1.W3', 'D3' : {'M': 't in D1.D3.M'}}, 'W2': 't in W2', 'D2' : {'M' : 't in D2.M', 'W1' : 't in D2.W1', 'D1' : {'M' : 't in D2.D1.M'}, 'W2' : 't in D2.W2', 'D2': {'M': 't in D2.D2.M', 'W1': 't in D2.D2.W1', 'D1' : {'M': 't in D2.D2.D1.M'}, 'W2' : 't in D2.D2.W2', 'D2' : {'M': 't in D2.D2.D2.M'}, 'W3' : 't in D2.D2.W3', 'D3' : {'M' : 't in D2.D2.D3.M'}}}}



d2 = {'W1' : ['PushButton', 'isPressed'], 'D1' : {'M' : ['LED_Group', 'current', 'off'], 'W1' : '1', 'D1' : {'M' : ['LED_Group', 'next', 'on']}}}

d3 = {'W1' : ['!', 'PushButton', 'isPressed'], 'D1' : {'M' : ['LED_Group', 'current', 'off'], 'W1' : '1', 'D1' : {'M' : ['LED_Group', 'next', 'on']}}, 'W2' : ['LED', 'isOn'], 'D2' : {'M' : ['None']}}

d4 = {'W1': 't in W1', 'D1' : {'M' : 't in D1.M', 'W1' : 't in D1.W1', 'D1' : {'M' : 't in D1.D1.M'}, 'W2' : 't in D1.W2', 'D2': {'M': 't in D1.D2.M', 'W1': 't in D1.D2.W1', 'D1' : {'M': 't in D1.D2.D1.M'}, 'W2' : 't in D1.D2.W2', 'D2' : {'M': 't in D1.D2.D2.M'}, 'W3' : 't in D1.D2.W3', 'D3' : {'M' : 't in D1.D2.D3.M'}}, 'W3': 't in D1.W3', 'D3' : {'M': 't in D1.D3.M'}}}

s1 = [['servo1', 'init', '9'], ['LED1', 'init', '3'], ['LED2', 'init', '5'], ['LED3', 'init', '6']]

i1 = [['B_Servo', 'servo1'], ['B_LED', 'LED1'], ['B_LED', 'LED2'], ['B_LED', 'LED3'], ['B_LEDGroup', 'LED_Group1', 'LED1', 'LED2', 'LED3']]

d4 = {'W1':['PB1', 'is_on'], 'D1': {'M': ['LED1', 'turn_on']}, 'W2': ['!', 'PB1', 'is_on'], 'D2' : {'M' : ['LED1', 'turn_off']}}
s4 = [['B_PushButton', 'PB1'], ['B_LED', 'LED1']]
i4 = [['PB1', 'init', '9'], ['LED1', 'init', '4']]

c1 = Compiler(d4, s4, i4)

c1.build()