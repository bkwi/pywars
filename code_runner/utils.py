output_separator = '---json-response-below---'

test_code_template = '''
import json

$solution

statements = $test_statements

response = {'passed': True, 'msg': '', 'action': 'test_result'}

for statement in statements:
    try:
        if eval(statement) is not True:
            raise Exception('Statement %s is not True' % statement)
    except Exception as e:
        response['passed'] = False
        response['msg'] = e.message
        break

print '$separator'
print json.dumps(response)
'''

validation_code = '''$solution

import json

print '$separator'
print json.dumps({'valid': True})
'''
