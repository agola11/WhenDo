from compiler import Compiler
d1 = {'W1': 't in W1', 'D1' : {'M' : 't in D1.M', 'W1' : 't in D1.W1', 'D1' : {'M' : 't in D1.D1.M'}, 'W2' : 't in D1.W2', 'D2': {'M': 't in D1.D2.M', 'W1': 't in D1.D2.W1', 'D1' : {'M': 't in D1.D2.D1.M'}, 'W2' : 't in D1.D2.W2', 'D2' : {'M': 't in D1.D2.D2.M'}, 'W3' : 't in D1.D2.W3', 'D3' : {'M' : 't in D1.D2.D3.M'}}, 'W3': 't in D1.W3', 'D3' : {'M': 't in D1.D3.M'}}, 'W2': 't in W2', 'D2' : {'M' : 't in D2.M', 'W1' : 't in D2.W1', 'D1' : {'M' : 't in D2.D1.M'}, 'W2' : 't in D2.W2', 'D2': {'M': 't in D2.D2.M', 'W1': 't in D2.D2.W1', 'D1' : {'M': 't in D2.D2.D1.M'}, 'W2' : 't in D2.D2.W2', 'D2' : {'M': 't in D2.D2.D2.M'}, 'W3' : 't in D2.D2.W3', 'D3' : {'M' : 't in D2.D2.D3.M'}}}}


i1 = ['PushButton', 'isPressed']

d2 = {'W1' : ['PushButton', 'isPressed'], 'D1' : {'M' : ['LED_Group', 'current', 'off'], 'W1' : '1', 'D1' : {'M' : ['LED_Group', 'next', 'on']}}}

d3 = {'W1' : ['PushButton', 'isPressed'], 'D1' : {'M' : ['LED_Group', 'current', 'off'], 'W1' : '1', 'D1' : {'M' : ['LED_Group', 'next', 'on']}}, 'W2' : ['LED', 'isOn'], 'D2' : {'M' : ['Serial','println']}}

d4 = {'W1': 't in W1', 'D1' : {'M' : 't in D1.M', 'W1' : 't in D1.W1', 'D1' : {'M' : 't in D1.D1.M'}, 'W2' : 't in D1.W2', 'D2': {'M': 't in D1.D2.M', 'W1': 't in D1.D2.W1', 'D1' : {'M': 't in D1.D2.D1.M'}, 'W2' : 't in D1.D2.W2', 'D2' : {'M': 't in D1.D2.D2.M'}, 'W3' : 't in D1.D2.W3', 'D3' : {'M' : 't in D1.D2.D3.M'}}, 'W3': 't in D1.W3', 'D3' : {'M': 't in D1.D3.M'}}}

c1 = Compiler(d3)

c1.build()