opcode = { "CLA" : "0000", "LAC" : "0001", "SAC": "0010" , "ADD" : "0011", "SUB": "0100", "BRZ": "0101", "BRN": "0110", "BRP": "0111", "INP" : "1000", "DSP": "1001", "MUL": "1010", "DIV": "1011", "STP": "1100"}
pc = 0
inst_table = []
symbol_table = []
temp_table = []

def in_list(item,L):
    for i in L:
    	if(len(i)>1):
	        if (item in i ):
	            return L.index(i)
    return -1

#read input file

f = open("inp1.txt","r")
q=0
p=0

for line in f:
	l = line.lstrip(' ')  #removing leading spaces
	b = l.split("#")[0]
	a = b.split()

	t=0

	if(0<len(a)<4):

		if (a[0]=="START"):
			if(len(a)==1):
				pc = 0
			else:
				pc = int(a[1])
			

		elif(a[0]!="END"):
			if(len(a)==1):
				if a[0] in opcode.keys():
					inst_table.append([a[0],pc]);
			if(len(a)>1 and a[1]!="DEC"):

				if(len(a)==3):                                #Error Handling - no of operands greater than 1
					if a[0] in opcode.keys():
						p=-1
				for i in range(len(a)):
					t=0
					if(i==0):
						if a[i] in opcode.keys():
							inst_table.append([a[i],pc])
						else:
							symbol_table.append([a[i],pc])  #label - with pc (add only if not present in the symbol table

					if(i==1):
						if a[i] in opcode.keys():
							inst_table.append([a[i],pc])
						else:
							if (len(symbol_table)>0):
								for r in range(len(symbol_table)):
									if a[i]  != symbol_table[r][0]:
										t+=1


								if(t==len(symbol_table)):
									symbol_table.append([a[i]]) #label or variable without pc
									   

							else:
								symbol_table.append([a[i]])
					if(i==2):
						if(len(symbol_table)>0):
							for s in range(len(symbol_table)):
								if a[i]  != symbol_table[s][0]:
									t+=1
							if(t==len(symbol_table)):
								symbol_table.append([a[i]])

						else:
							symbol_table.append([a[i]])
			else:
				for j in range(len(symbol_table)):
					if a[0] == symbol_table[j][0]:
						symbol_table[j].append(pc)



			pc+=1

	if(len(a)>3):
		q=-1


new_f = open("inp1.txt","r")
dec_prob = 0
not_dec = []
m=0
y=0

def check_dec_label_var(element):                            # Error Handling - if a label or variable is not declared
	m=0
	if(len(not_dec)>0):
		for el in not_dec:
			if element != el:
				m+=1
		if(m==len(not_dec)):
			not_dec.append(element)

	else:
		not_dec.append(element)
	                                                      

for line1 in new_f:
	l = line1.lstrip(' ')  #removing leading spaces
	b = l.split("#")[0]
	a = b.split()

	if(len(a)>0):
		if (a[0]=="START"):
			continue

		elif(len(a)>1 and a[1] != "DEC"):
			if (len(a)==2):
				if(a[1]=="CLA" or a[1]=="STP"):
					temp_table.append([opcode.get(a[1])]);
				else:
					opcode_binary = opcode.get(a[0])
					index2 = in_list(a[1],symbol_table)
					
					if index2== -1:
						check_dec_label_var(a[1])
						                                        # Error Handling - if a label or variable is not declared
						dec_prob = -1

					if len(symbol_table[index2])>1:
						address = symbol_table[index2][1]
						address_bin = format(address, '08b')
						temp_table.append([opcode_binary,address_bin])
					
			elif (len(a)==3):
				opcode_binary = opcode.get(a[1])
				index2 = in_list(a[2],symbol_table)

				if index2== -1:
					check_dec_label_var(a[2])
					                                        # Error Handling - if a label or variable is not declared
					dec_prob = -1

				if len(symbol_table)>1:
					address = symbol_table[index2][1]
					address_bin = format(address, '08b')
					temp_table.append([opcode_binary,address_bin])

		elif (len(a)==1 and a[0]!="END"):
				opcode_t = opcode.get(a[0])
				if (opcode_t == "0000"):
					temp_table.append([opcode_t])
				elif (opcode_t == "1100"):
					temp_table.append([opcode_t])
				else:
					y=-1                                        #Error Handling - 0 operands given (opcode not CLA or STP)


op = 0
lab = 0
end =0
start = 0
for j in range(len(temp_table)):                        #Error Handling - Invalid opcode name
	if temp_table[j][0] != None:
		op+=1

for ele in symbol_table:
	if len(ele)==1:
		symbol_table.remove(ele)

for s in range(len(symbol_table)):                      #Error Handling - defined label names used as a variable and vice versa
	if (len(symbol_table[s])>2):
		lab = -1

file1 = open("inp1.txt","r")                            #Error Handling - END Statement not present
lineList = file1.readlines()
file1.close()
for u in lineList:
	if(u=='\n'):
		lineList.remove(u)
x = lineList[0]
x_1 = x.split()
if (x_1[0] != "START"):
	start = -1 
if (lineList[len(lineList)-2] != "END\n"):
	end = -1

with open('output.txt', 'w') as filehandle:
	if (op==len(temp_table) and dec_prob!= -1 and lab==0 and pc<256 and q==0 and p==0 and end==0 and start==0 and y==0):
		print("Symbol table - ", symbol_table)
		print("Opcode table - " ,inst_table)
		print("Combined table after 2nd pass- ",temp_table)
		for l in range(len(temp_table)):
			if(len(temp_table[l])==1):
				filehandle.write('%s\n' % (temp_table[l][0]))
			else:
				filehandle.write('%s\n' % (temp_table[l][0] + "   " + temp_table[l][1]))

	if(start==-1):
		print("START of program not found")
		filehandle.write('%s\n' %"START of program not found")

	elif(end==-1):
		print("END of program not found")
		filehandle.write('%s\n' %"END of program not found")

	else:

		if(op!=len(temp_table)):
			print("Invalid opcode name")
			filehandle.write('%s\n' %"Invalid opcode name")

		if(q==-1):
			print("ERROR - Invalid statement")
			filehandle.write('%s\n' %("ERROR - Invalid statement"))

		if(dec_prob==-1):
			for e in not_dec:
				print(e + " is not declared")
				filehandle.write('%s\n' %(e + " is not declared"))

		if(lab==-1):
			print("ERROR - Defined label names cannot be used as variable names and vice versa")
			filehandle.write('%s\n' %("ERROR - Defined label names cannot be used as variable names and vice versa"))

		if(pc>=256):
			print("ERROR - Address supplied out of bounds")
			filehandle.write('%s\n' %("ERROR - Address supplied out of bounds"))

		if(p==-1):
			print("ERROR - Number of operands supplied greater than 1")
			filehandle.write('%s\n' %("ERROR - Number of operands supplied greater than 1"))

		if(y==-1):
			print("ERROR - zero operand provided")
			filehandle.write('%s\n' %("ERROR - zero operand provided"))

	










