# f = open('demo.txt',mode='r')
# # f.write('add this content!\n')
# # file_content = f.readlines()
# # f.close()

# # for line in file_content:
# #     print(line[:-1])
# line = f.readline()
# while line:
#     print(line)
#     line = f.readline()

# f.close()

with open('demo.txt',mode='r') as f:
    line = f.readline()
    while line:
        print(line)
        line = f.readline()
print('done!')