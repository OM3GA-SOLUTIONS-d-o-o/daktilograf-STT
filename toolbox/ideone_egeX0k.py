def countLetter(n):
    p=['','jedan','dva','tri','četiri','pet','šest','sedam','osam','devet']
    q=['','deset','dvadeset','trideset','četrdeset','pedeset','šezdeset','sedamdeset','osamdeset','devedeset']
    r=['','jedanaest','dvanaest','trinaest','četrnaest','petnaest','šesnaest','sedamnaest','osamnaest','devetnaest']

    c=str(n)
    l=len(c)
    a=""

    if l==1:
        a+=p[int(c[0])]
    elif l==2:
        if c[1]=='0':
            a+=q[int(c[0])]
        elif c[0]=='1':
            a+=r[int(c[1])]
        else:
            a+=q[int(c[0])]+p[int(c[1])]
    elif n==100:
        a+="jednastotina"
    elif l==3:
        a+=p[int(c[0])]+"stotina"
        if c[1]=='0' and c[2]=='0':
            a+=""
        elif c[2]=='0' and c[1]!='0':
            a+="i"+q[int(c[1])]
        elif c[1]=='1':
            a+="i"+r[int(c[2])]
        else:
            a+="i"+q[int(c[1])]+p[int(c[2])]
    else:
        a+="jednahiljada"

    #print a,len(a)
    return len(a)

def main():
    sum=0
    for i in range(1,1001):
        sum+=countLetter(i)
    print sum

main()
