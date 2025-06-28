from cProfile import run
from concurrent.futures import process
import math
from operator import countOf
import os
from tkinter import filedialog

def need_memory(num):   # 필요한 메모리 칸 수
    return math.ceil(p_size[num] / offset_size)

def search_mem(p): # 메모리에 공간이 있는지 탐색
    if p == len(p_size):
        return 'full'
    for j in range(0, memory_length-need_memory(p)+1):
        m = j
        memory_count = 0
        for i in range(0, need_memory(p)):
            if memory[m] == '':
                memory_count += 1
            m += 1

        if memory_count == need_memory(p):
            m = m - need_memory(p)
            return m
    return 'full'  

def add_mem(p, m): # 메모리에 탑재
    for k in range(0, need_memory(p)):
        memory[m] = 'P%d, %s, %s, T%d~T%d' %(p, bin(k)[2:].zfill(page_bit), bin(m)[2:].zfill(page_bit), now_time, now_time + p_time[p])
        m += 1
    process_state[p] = '실행중T%d' %(now_time+p_time[p])
    running_time.append(p_time[p])
    state_time.append(now_time+p_time[p])

def print_mem(): # 파일에 메모리 내용 WRITE
    new_file.write('************************\n')
    new_file.write('** T=%d Paging Table **\n' %now_time)
    for i in range(0, len(memory)):
        if memory[i] != '':
            new_file.write(memory[i]+'\n')
        else:
            new_file.write(' - , - , %s , - \n' %bin(i)[2:].zfill(page_bit))

def print_process(): # 파일에 프로세스 진행상태 WRITE
    new_file.write('** T=%d Process State **\n' %now_time)
    for index, value in enumerate(process_state):
        if '실행중' in value:
            new_file.write('P%d, 실행중, %d개 Page사용\n' %(index, need_memory(index)))
        if value == '미실행':
            new_file.write('P%d, 미실행\n' %index)
        if value == '실행종료':
            new_file.write('P%d, 실행종료\n' %index)
    

def delete_mem(): # 실행이 끝난 메모리 삭제
    for index, value in enumerate(process_state):
        if 'T%d' %now_time in value:
            process_state[index] = '실행종료'

            for i in range(0, memory_length):
                if 'P%d' %index in memory[i]:
                    memory[i] = ''


read_path = filedialog.askopenfilenames(initialdir="./txt",\
                 title = "파일을 선택 해 주세요",\
                    filetypes = (("txt files", "*.txt"),))[0]        #files 변수에 선택 파일 경로 넣기

write_path = read_path[:-4] + '_result.txt'

new_file = open(write_path, 'w')

print(read_path)    #읽을 파일의 경로 출력

text = open(read_path, 'r') #파일 읽기
lines = text.readlines()
line = text.readline()

p_size = ['']
p_time = ['']
state_time = [0]
memory = []
process_state = ['']
running_time = [0]
memory_count = 0


for line in lines:
    line = line.replace(',', ' ')
    line_token = []
    line_token = line.split()

    head = line_token[0]

    print(line_token)

    if head == 'Page':
        page_bit = int(line_token[2])
        memory_length = 2 ** page_bit
        memory = [''] * memory_length

    elif head == 'Offset':
        offset_size = 2 ** int(line_token[2])    

    elif len(line_token[0]) == 2:
        p_size.append(int(line_token[1]))
        p_time.append(int(line_token[2]))
        process_state.append('미실행')

p = 1
r = 0
time = min(running_time)
now_time = min(state_time)
state_time.remove(min(state_time))
running_time.remove(min(running_time))

while process_state.count('실행종료') <= len(process_state)-1:
    r+=1
    m = 0
    while m != 'full':
        m = search_mem(p)
        if m != 'full':
            add_mem(p, m)
            p += 1

    print_mem()
    print_process()
    
    if process_state.count('실행종료') >= len(process_state)-1: break

    time = min(running_time)
    now_time = min(state_time)

    while now_time in state_time:
        state_time.remove(now_time)
    
    running_time.remove(min(running_time))
    
    delete_mem()
new_file.write('** 20181312, 김대현 **\n\n')
    
# m = 0
# while m != 'full':
#     m = search_mem(p)
#     if m != 'full':
#         add_mem(p, m)
#         p += 1

# print_mem()
# print_process()

new_file.close