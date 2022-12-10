num_col = 5
em =    "                |"
em_row = [em]*len_row
a = "aaaaaaa         |"
names = [a]*len_row

line =     "-----------------"
arrow_r  = "-->             |"
arrow_l  = "   <-------------"
line_r  =  "   --------------"
line_l  =  "---             |"
row1 = [a, em, em, em, em, em]
row2 = [em, a, em, em, em, em]
row3 = [em, em, a, em, em, em]
row4 = [em, em, em, a, em, em]
row5 = [em, em, em, em, a, em]
row6 = [em, em, em, em, em, a]

arrows={
"arrow01" : [line_r,arrow_r,em,em ],
"arrow02" : [line_r,line,arrow_r, em],
"arrow03" : [line_r, line, line, arrow_r],
"arrow12" : [em, line_r, arrow_r, em],
"arrow13" : [em, line_r, line, arrow_r],
"arrow23" : [em,em,line_r, arrow_r],
"arrow10" : [arrow_l, line_l, em, em],
"arrow20" : [arrow_l, line, line_l, em],
"arrow30" : [arrow_l, line, line, line_l],
"arrow21" : [em, arrow_l, line_l, em],
"arrow31" : [em, arrow_l, line, line_l],
"arrow32" : [em, em, arrow_l, line_l]
}
log = []
log.append(names)
log.append(em_row)
log.append(row1)
log.append(row3)
log.append(row3)
log.append(row1)
log.append(row1)
log.append(row6)
log.append(row2)
log.append(row2)
log.append(row3)
log.append(row1)
log.append(row1)
log.append(row5)
log.append(row3)
log.append(row4)
log.append(row2)
log.append(row4)
log.append(row2)
log.append(row2)
log.append(row6)
log.append(row3)
log.append(row3)
log.append(row1)
log.append(row1)
log.append(row4)
log.append(row2)
log.append(row2)
log.append(row3)
log.append(row1)
'''                    
def prt_log( log):
    for r in range(len(log)-1):
        row = log[r]
        row2 = log[r+1]
        print("".join(row))
        p1 = 0
        p2 = 0
        for i in range(len(row)):
            if row[i] != em:
                p1 = i
        for j in range( len(row2)):
            if row2[j] != em:
                p2 = j
        if p1 != p2 and r > 1:
            sr = "arrow"+str(p1)+str(p2)
            print("".join(arrows[sr]))
    print("".join(log[-1]))
        
'''        
        
def arrow_row(a, b):
    if any([a<0, b<0, a>num_col, b>num_col]):
        return False
    row = []
    if a<b:
        for i in range(num_col):
            if i<a or i>b:
                row.append(em)
            elif i>a and i < b:
                row.append(line)
            elif i == a:
                row.append(line_r)
            elif i == b:
                row.append(arrow_r)
    elif a>b:
        for i in range(num_col):
            if i>a or i<b:
                row.append(em)
            elif i<a and i > b:
                row.append(line)
            elif i == a:
                row.append(line_l)
            elif i == b:
                row.append(arrow_l)
                            
    print("".join(row))
    
def pr_log( log):
    for r in range(len(log)-1):
        row = log[r]
        row2 = log[r+1]
        print("".join(row))
        p1 = 0
        p2 = 0
        for i in range(num_col):
            if row[i] != em:
                p1 = i
        for j in range( num_col):
            if row2[j] != em:
                p2 = j
        if p1 != p2 and r > 1:
            arrow_row(p1, p2)

    print("".join(log[-1]))
    
'''
a = 0
b = 2

arrow_row(a, b)
for i in range(6):
    arrow_row(i, 0)
 '''   
print()
pr_log(log)


    
    
#prt_log(log)   