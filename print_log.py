import config

log = config.log

num_col = config.num_col
spase = config.spase
class_names = config.class_names
em_row = [spase]*num_col
a = "  aaaaaaa         |"
#names = [a]*num_col


spase =    "                  |"
line =     "-------------------"
arrow_r  = "-->               |"
arrow_l  = "    <--------------"
line_r  =  "    ---------------"
line_l  =  "---               |"
row1 = [a, spase, spase, spase, spase, spase]
row2 = [spase, a, spase, spase, spase, spase]
row3 = [spase, spase, a, spase, spase, spase]
row4 = [spase, spase, spase, a, spase, spase]
row5 = [spase, spase, spase, spase, a, spase]
row6 = [spase, spase, spase, spase, spase, a]



#log.append(names)
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
            if row[i] != spase:
                p1 = i
        for j in range( len(row2)):
            if row2[j] != spase:
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
                row.append(spase)
            elif i>a and i < b:
                row.append(line)
            elif i == a:
                row.append(line_r)
            elif i == b:
                row.append(arrow_r)
    elif a>b:
        for i in range(num_col):
            if i>a or i<b:
                row.append(spase)
            elif i<a and i > b:
                row.append(line)
            elif i == a:
                row.append(line_l)
            elif i == b:
                row.append(arrow_l)
                            
    print("".join(row))
    
def pr_log():
    for r in range(len(log)-1):
        row = log[r]
        row2 = log[r+1]
        print("".join(row))
        p1 = 0
        p2 = 0
        for i in range(num_col):
            if row[i] != spase:
                p1 = i
        for j in range( num_col):
            if row2[j] != spase:
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
pr_log()


    
    
#prt_log(log)   