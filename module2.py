def writeValue(addrName, addr): # 주소 이름을 변수로 하여 주소를 저장
    globals() [addrName] = addr


def readValue(addrName): # 주소 이름에 해당하는 주소를 리턴
    return globals() [addrName]

# 가상의 HighLevel Language 로 작성된 .pl (programming language) 코드를
# 가상의 LowLevel Language 의 .bi (binary) 코드로 변환하는 컴파일러 모듈

root_path = 'F:/PythonStudy/module/'
while True:
    file_name = input('Input File: ')
    read_path = root_path + file_name #읽을 파일 경로

    try:
        text = open(read_path, 'r') #파일 읽기
        break

    except FileNotFoundError: # 파일 없음
        print(f"'{file_name}' 해당 파일이 존재하지 않습니다.")


write_path = root_path + file_name[:-2] + 'bi' #출력 파일 경로



lines = text.readlines()
line = text.readline()

new_file = open(write_path, 'w') #출력할 파일 생성

for line in lines:
    line = line.replace(',', ' ')
    line_token = []
    line_token = line.split() #tokenize

    opcode = line_token[0]
    opr1 = line_token[1]
    if len(line_token) >= 3:
        opr2 = line_token[2]
        if len(line_token) >= 4:
            opr3 = line_token[3]

    print(line_token)

    if opcode == 'WRITE': #WRITE
        new_file.write('0011 ' + opr3 + '\n')
        new_file.write('1000 ' + opr2 + '\n')
        new_file.write('0101\n')
        writeValue(opr1, opr2)

    elif opcode == 'STORE': #STORE
        temp = readValue(opr1)
        new_file.write('0010 ' + temp + '\n')

    elif opcode == 'PRINT': #PRINT
        temp = readValue(opr1)
        new_file.write('1001 ' + temp + '\n')

    elif opcode == 'ADD': #ADD
        if opr2.isalpha() == True:
            temp1 = readValue(opr1)
            temp2 = readValue(opr2)

            new_file.write('0001 ' + temp1 + '\n')
            new_file.write('0100\n')
            new_file.write('0001 ' + temp2 + '\n')
            new_file.write('0110\n')
            new_file.write('0101\n')
        
        else: # 상수와의 연산일 경우
            temp1 = readValue(opr1)
            temp2 = format(int(opr2), 'b').zfill(4)

            new_file.write('0001 ' + temp1 + '\n')
            new_file.write('0100\n')
            new_file.write('0000 ' + temp2 + '\n')
            new_file.write('0110\n')
            new_file.write('0101\n')

    elif opcode == 'SUB': #SUB
        if opr2.isalpha() == True:
            temp1 = readValue(opr1)
            temp2 = readValue(opr2)

            new_file.write('0001 ' + temp1 + '\n')
            new_file.write('0100\n')
            new_file.write('0001 ' + temp2 + '\n')
            new_file.write('0111\n')
            new_file.write('0101\n')
        
        else: # 상수와의 연산일 경우
            temp1 = readValue(opr1)
            temp2 = format(int(opr2), 'b').zfill(4)

            new_file.write('0001 ' + temp1 + '\n')
            new_file.write('0100\n')
            new_file.write('0000 ' + temp2 + '\n')
            new_file.write('0111\n')
            new_file.write('0101\n')

print(f'bi File Created. {new_file.name}')
print('COMPLETE')
text.close #파일 닫기
new_file.close