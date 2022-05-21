def get_input() -> list:
    """
    print sytax
    print examples
    get line input
    break line into list

    {'class': '', 'semester': '', 'prefix': '', 'from': '', 'to': ''}
    """
    
    order = ['class', 'semester', 'prefix', 'from', 'to']

    # syntax = [ {'class': '{ [D]DMCA | [M]CA }', 'semester': '{ 1|2|3|4|5|6|7|8 }',
        # 'prefix': '$Enrollment_number_common_part', 
        # 'from': '$Enrollment_number_range_start', 'to': '$Enrollment_number_range_end'} ]
    # for i in range(len(syntax)):
    #     for v in order:
    #         print(syntax[i][v], end=' ')
    #         # print(i, end=' ')
    #     print()

    examples = [
        {'class': 'DDMCA', 'semester': '5', 'prefix': '0827CA19DD', 'from': '1', 'to': '3'},
        {'class': 'DDMCA', 'semester': '1', 'prefix': '0827CA21DD', 'from': '10', 'to': '20'},
        {'class': 'MCA', 'semester': '2', 'prefix': '08XXX', 'from': '5', 'to': '15'},
    ]

    print('\nINPUT FORMAT')
    print('$' + ' $'.join(order))
    print('Press Ctrl+c to abort.')
    print("\nExamples:")
    for i, d in enumerate(examples):
        print(' '.join(examples[i].values()))
        # print(' '.join(d))
    print()
    inp = input(">>? ")
    return { k:v for (k,v) in zip(order, inp.split(' ')) }

def validate(inputList : list) -> bool:

    import re


    rePattern = r'(D(D(M(CA?)?)?)?)|(M(CA?)?)'
    branch = re.compile(rePattern, re.I)
    if(not branch.match(inputList['class'])):
        print('Invalid input: $branch can be one of { DDMCA, MCA }')
        return False
    try:
        inputList['from']       = int(float(inputList['from']))
        inputList['to']         = int(float(inputList['to']))
        inputList['semester']   = int(float(inputList['semester']))
    except ValueError:
        print('Invalid input: $from or $to or $semester value not a number.')
        return False
    else:
        if(inputList['semester'] not in range(1, 11)): 
            print('Invalid input: 1 <= $semester <= 10')
            return False
        return True

def enrgenerator(pre, frm, to):
    list=[]
    pre=pre.upper()
    for n in range(frm, to + 1):
        if n < 10:
            list.append(pre + '0' + str(n))
        else:
            list.append(pre + str(n))
    return list

def confirm(inputList : list) -> bool:
    """
    Confirm if user doesn't want to re-enter the input.
    """
    branches = { 'D': 'DDMCA', 'M': 'MCA' }
    branch = branches[inputList['class'][0].upper()]
    frm = int(float(inputList['from']))
    to = int(float(inputList['to']))
    listLen = to - frm + 1
        
    for i in range(frm, frm + min(6, listLen)):
        print(inputList['prefix'] 
            + (f'0{i}' if (i < 10) else str(i) )
            + f"\t\tfrom {branch} {inputList['semester']}")
            
    if(listLen > 6):
        print('...')
        print(f"{inputList['prefix']}", end="") 
        print(f"0{to}" if (i < 10) else f"{to}")
    
    confirmation = True if \
        input("Re-input? (Y/N) [Default = N] ")[:1].lower() != 'y' \
            else False

    return confirmation

if __name__ == '__main__':
    lst = get_input()
    print("out of get_input()")
    for i in lst:
        print(i, end=" ")
    # print(2 in range(1, 5))