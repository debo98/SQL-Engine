import csv
import sys

DATA={}

def Meta_Read():
    ret={}
    file=open('./metadata.txt','r')
    begin=-1
    for line in file:
        proc_line=line.strip()
        if proc_line=="<begin_table>":
            begin=0
        else:
            if begin==0:
                tag=proc_line
                ret[tag]=[]
                begin=1
            else:
                if proc_line=="<end_table>":
                    begin=-1
                else:
                    ret[tag].append(tag+'.'+proc_line)            
    return ret        

def Csv_Read(name):
    ret=[]
    with open(name, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            ret.append(row)
    csvFile.close()    
    return ret

def ReadAll(Meta):
    for key in Meta:
        j=key+'.csv'
        DATA[key]=Csv_Read(j)


def Where_Check(Info,label):
    for i in range(len(Info)-1):
        # print(Info[i])
        y=Info[i][0]
        
        if '.' in y:
            flag=0
            for lab in label:
                if y==lab:
                    flag=1
            if flag==0:
                print("ERROR: INCORRECT WHERE QUERY")
                return -1
        else:
            cnt=0
            for lab in label:
                if y==lab.split('.')[1]:
                    cnt+=1
                    change=lab
            if cnt==0:
                print("ERROR: INCORRECT WHERE QUERY")
                return -1                        
            if cnt==1:
                Info[i][0]=change
            if cnt>1:
                print("ERROR: AMBIGUITY IN WHERE QUERY")
                return -1                        
    return Info

def Where_Handler(Inp,Dict):
    Info=Inp
    x=0
    if 'AND' in Inp:
        x=1
        Info=Info.split('AND')
    else:   
        if 'OR' in Inp:
            x=2
        Info=Info.split('OR')
    ops=[]    
    # print(Info)
    for i in range(len(Info)):
        if '>=' in Info[i]:
            Info[i]=Info[i].split('>=')
            ops.append('>=')
            continue
        if '<=' in Info[i]:
            Info[i]=Info[i].split('<=')
            ops.append('<=')
            continue        
        if '<' in Info[i]:
            Info[i]=Info[i].split('<')
            ops.append('<')
            continue
        if '>' in Info[i]:
            Info[i]=Info[i].split('>')
            ops.append('>')
            continue        
        if '=' in Info[i]:
            Info[i]=Info[i].split('=')
            ops.append('=')
            continue
    if len(ops)==0:
        print("ERROR: INCORRECT WHERE QUERY")
        return -1,-1

    for i in range(len(Info)):
        for j in range(len(Info[i])):
            Info[i][j]=Info[i][j].strip(' ')
    
                


    Info.append(x)

    # print("#############")
    # print(Info)
    # print("#############")
    return Info,ops        

def Make_Unique(Inp):
    ret=[]
    mrk=[]
    Inp1=[]
    for j in range(len(Inp[0])):
        x=[]
        for i in range(len(Inp)):
            x.append(Inp[i][j])
        Inp1.append(x)    

    for i in range(len(Inp1)):
        mrk.append(0)

    
    for i in range(len(Inp1)):
        if mrk[i]==0:
            for j in range(i+1,len(Inp1)):
                if Inp1[i]==Inp1[j]:
                    mrk[j]=1    

    Inp2=[]

    for i in range(len(Inp1)):
        if mrk[i]==0:
            Inp2.append(Inp1[i])

    ret=[]                
    for j in range(len(Inp2[0])):
        x=[]
        for i in range(len(Inp2)):
            x.append(Inp2[i][j])
        ret.append(x)                    
    return ret        

def Where_Filter(table,Info,ops,label):
    ret_form=[]    
    Digits=['0','1','2','3','4','5','6','7','8','9']
    for i in range(len(table)):
        for j in range(len(table[0])):
            table[i][j]=int(table[i][j])
    glob=0        
    for i in range(len(table)):
        if Info[len(Info)-1]==0:
            flg=0
            for it in Info[0][1]:
                if it not in Digits:
                    flg=1
            
            if Info[0][0] in label:
                idx=label.index(Info[0][0])
                if flg==0:        
                    val=int(Info[0][1])
                else:
                    # print("qef",Info[0][1],label)
                    if Info[0][1] in label:
                        idx1=label.index(Info[0][1])
                    else:
                        # print("weg")
                        print("ERROR: INCORRECT COLUMN")
                        return -1,-1       
                
                if ops[0]=='>=':
                    if table[i][idx]>=val:
                        ret_form.append(table[i])
                if ops[0]=='<=':
                    if table[i][idx]<=val:
                        ret_form.append(table[i])
                if ops[0]=='>':
                    if table[i][idx]>val:
                        ret_form.append(table[i])
                if ops[0]=='<':                
                    if table[i][idx]<val:
                        ret_form.append(table[i])
                if ops[0]=='=':
                    if flg==0:
                        if table[i][idx]==val:
                            ret_form.append(table[i])
                    else:
                        glob=1
                        if table[i][idx]==table[i][idx1]:
                            ret_form.append(table[i])        
            else:
                print("ERROR: INCORRECT COLUMN")
                return -1,-1    
        else:
            if Info[0][0] in label and Info[1][0] in label:
                idx,idx1=label.index(Info[0][0]),label.index(Info[1][0])
                flag,flag1=0,0
                try:
                    val=int(Info[0][1])
                except:
                    val=table[i][label.index(Info[0][1])]
                try:
                    val1=int(Info[1][1])
                except:
                    val1=table[i][label.index(Info[1][1])]
                if ops[0]=='>=':
                    if table[i][idx]>=val:
                        flag=1
                if ops[0]=='<=':
                    if table[i][idx]<=val:
                        flag=1
                if ops[0]=='>':
                    if table[i][idx]>val:
                        flag=1
                if ops[0]=='<':                
                    if table[i][idx]<val:
                        flag=1
                if ops[0]=='=':
                    if table[i][idx]==val:
                        flag=1
                if ops[1]=='>=':
                    if table[i][idx1]>=val1:
                        flag1=1
                if ops[1]=='<=':
                    if table[i][idx1]<=val1:
                        flag1=1
                if ops[1]=='>':
                    if table[i][idx1]>val1:
                        flag1=1
                if ops[1]=='<':                
                    if table[i][idx1]<val1:
                        flag1=1
                if ops[1]=='=':
                    if table[i][idx1]==val1:
                        flag1=1

                if flag&flag1 == 1 and Info[len(Info)-1]==1:
                    ret_form.append(table[i])        
                if flag|flag1 == 1 and Info[len(Info)-1]==2:
                    ret_form.append(table[i])

                    
            else:
                print("ERROR: INCORRECT COLUMN IN WHERE CLAUSE")
                return -1,-1           
    to_be_deleted=""
    if glob:
        to_be_deleted=Info[0][0]            
    return ret_form,to_be_deleted    

            
def Type1(Inp,Dict,dist,Info,ops):
    delt=''
    S=''
    for i in Inp:
        S+=i
    S=S.split(',')

    for i in range(len(S)):
        if S[i] not in Dict:
            print("ERROR: NO SUCH TABLE IN DATABASE")
            return

    if len(S)==1:
        label=[]
        for key in Dict[S[0]]:
            label.append(key)
        Mat=DATA[S[0]]
        if len(Info)!=0:
            P=Where_Check(Info,label)
            if P==-1:
                return
            else:
                Info=P         
            J,delt=Where_Filter(Mat,Info,ops,label)            
            if J==-1:
                return
            else:
                Mat=J

        for key in range(len(Dict[S[0]])-1):
            print(Dict[S[0]][key],end=',')
        print(Dict[S[0]][-1],end=' ')
        print()    
        if dist==1:
            Mat=Make_Unique(Mat)
        for i in range(len(Mat)):
            for j in range(len(Mat[0])-1):
                print(Mat[i][j],end=',')
            print(Mat[i][j],end=' ')
            print()    
    else:
        label=[]
        for key in Dict[S[0]]:
            label.append(key)
        
        table=DATA[S[0]]
        for i in range(1,len(S)):
            L1=[]
            for key in Dict[S[i]]:
                L1.append(key)
            table,label=JoinTable(table,DATA[S[i]],label,L1)

        if len(Info)!=0:    
            P=Where_Check(Info,label)
            if P==-1:
                return
            else:
                Info=P
            J,delt=Where_Filter(table,Info,ops,label)            
            if J==-1:
                return
            else:
                table=J

        ind=-1        
        ptr=-1        
        for i in range(len(label)-1):
            ptr+=1
            if delt == label[i]:
                ind=ptr
            else:    
                print(label[i],end=',')
        ptr+=1
        if delt == label[len(label)-1]:
            ind=ptr
        else:    
            print(label[-1],end=' ')
        print()
    
        
        if dist==1:
            table=Make_Unique(table)

        for i in range(len(table)):
            for j in range(len(table[0])-1):
                if ind != j:
                    print(table[i][j],end=',')
            if ind != len(table[0])-1:
                print(table[i][len(table[0])-1],end=' ')
            print()                


def Type2(Inp,String,Dict,dist,Info,ops):
    delt=''
    S=''
    for i in Inp:
        S+=i
    S=S.split(',')
    
    for i in range(len(S)):
        if S[i] not in Dict:
            print("ERROR: NO SUCH TABLE IN DATABASE")
            return
    label=[]
    for key in Dict[S[0]]:
        label.append(key)
    
    table=DATA[S[0]]
    for i in range(1,len(S)):
        L1=[]
        for key in Dict[S[i]]:
            L1.append(key)
        table,label=JoinTable(table,DATA[S[i]],label,L1)


    if len(Info)!=0:  
        P=Where_Check(Info,label)
        if P==-1:
            return
        else:
            Info=P
                  

        # print(label)            
        J,delt=Where_Filter(table,Info,ops,label)            
        # print(J,"ewg")
        if J==-1:
            return
        else:
            table=J    

    
    Cols=String.split(',')
    ret=[]
    # print(String)
    for i in Cols:
        if '.' in i:
            tmp=[]
            if i in label:
                idx=label.index(i)
                for j in range(len(table)):
                    tmp.append(table[j][idx])
                ret.append(tmp)
            else:
                print("ERROR: INCORRECT COLUMN")
                return 
        
        else:
            idx=0
            cnt=0
            ptr=-1
            # print(i)
            for j in label:
                ptr+=1
                k=j.split('.')[1]
                if k in i:
                    cnt+=1
                    idx=ptr
            if cnt == 0:
                print("ERROR:INCORRECT COLUMN")
                return
            if cnt >= 2:
                print("ERROR: AMBIGUITY IN COLUMNS")
                return
            if cnt == 1:
                tmp=[]
                try:
                    for itr in range(len(table)):
                        tmp.append(table[itr][idx])
                    ret.append(tmp)
                except:
                    print("ERROR: AMBIGUITY IN QUERY")
                    return    
    
    # print(delt)
    # print("###########################")                
    if dist==1:
        # print("weg")
        ret=Make_Unique(ret)        

    ind=-1
    ptr=-1    
    for i in range(len(Cols)-1):
        ptr+=1
        if delt == Cols[i]:
            ind=ptr
        else:
            print(Cols[i],end=',')
    ptr+=1
    if delt == Cols[-1]:
        ind=ptr
    else:
        print(Cols[-1],end=' ')
    print()
    

    for j in range(len(ret[0])):
        for i in range(len(ret)-1):
            if i != ind:
                print(ret[i][j],end=' ')
        if ind != len(ret)-1:
            print(ret[len(ret)-1][j],end=' ')
        print()    
    return    


def Type3(Inp,Aggs,Dict,dist,Info,ops):
    delt=''
    S=''
    for i in Inp:
        S+=i
    S=S.split(',')
    
    for i in range(len(S)):
        if S[i] not in Dict:
            print("ERROR: NO SUCH TABLE IN DATABASE")
            return


    ret=[]
    label=[]
    for key in Dict[S[0]]:
        label.append(key)
    
    table=DATA[S[0]]
    for i in range(1,len(S)):
        L1=[]
        for key in Dict[S[i]]:
            L1.append(key)
        table,label=JoinTable(table,DATA[S[i]],label,L1)

    # print(label)    
    if len(Info)!=0:    
        P=Where_Check(Info,label)
        if P==-1:
            return
        else:
            Info=P
        J,delt=Where_Filter(table,Info,ops,label)            
        if J==-1:
            return
        else:
            table=J    
    
    for i in Aggs:
        col=i[4:-1]

        if '.' in col:
            tmp=[]
            if col in label:
                idx=label.index(col)
                for j in range(len(table)):
                    tmp.append(table[j][idx])
                ret.append(tmp)
            else:
                print("ERROR: INCORRECT COLUMN")
                return 
        
        else:
            idx=0
            cnt=0
            ptr=-1
            for j in label:
                ptr+=1
                k=j.split('.')[1]
                if k==col:
                    cnt+=1
                    idx=ptr
            if cnt == 0:
                print("ERROR:INCORRECT COLUMN")
                return
            if cnt >= 2:
                print("ERROR: AMBIGUITY IN COLUMNS")
                return
            if cnt == 1:
                tmp=[]
                for itr in range(len(table)):
                    tmp.append(table[itr][idx])
                ret.append(tmp)    

    ptr=-1
    ind=-1
    for i in range(len(Aggs)-1):
        ptr+=1
        if delt == Aggs[i]:
            ind=ptr
        else:    
            print(Aggs[i],end=' ')
    ptr+=1
    if delt == Aggs[-1]:
        ind=ptr
    else:    
        print(Aggs[-1],end=' ')
    print()                 
    
    ans=[]
    for i in range(len(ret)):
        for j in range(len(ret[0])):
            ret[i][j]=int(ret[i][j])
        p=Aggs[i]
        if len(ret[i])==0:
            ans.append('NONE')
            continue
        if p[0:3]=='max':
            ans.append(max(ret[i]))
        if p[0:3]=='min':
            ans.append(min(ret[i]))
        if p[0:3]=='sum':
            ans.append(sum(ret[i]))
        if p[0:3]=='avg':
            ans.append(sum(ret[i])/len(ret[i]))
    
    if dist==1:
        ans=Make_Unique(ans)        

    for i in range(len(ans)-1):
        if ind != i:
            print(ans[i],end=' ')
    if ind != len(ans)-1:
        print(ans[-1],end=' ')
    print()        



def Query(Inp,Dict):
    Inp=Inp.replace(';','')
    Holder1=Inp.split(' ')
    Holder=[]
    for i in Holder1:
        if i!='':
            Holder.append(i)

    if 'Select' not in Holder or 'from' not in Holder:
        # print(Holder)
        print("ERROR: INCOMPLETE QUERY")
        return

    if Holder[0]!='Select':
        print("ERROR: INCOMPLETE QUERY")
        return
        
    pos_from=Holder.index('from')
    begin=1
    # print(begin,pos_from,Holder[begin])    
    S=''
    for i in range(begin,pos_from):
        S+=Holder[i]

    if "distinct" in Holder[1]  :
        begin+=1
    flag,cnt=0,0    
    J=S.split(',')
    for itr in J:
        if (itr[0:4]=='max(' and itr[-1:]==')') or (itr[0:4]=='min(' and itr[-1:]==')') or (itr[0:4]=='sum(' and itr[-1:]==')') or (itr[0:4]=='avg(' and itr[-1:]==')'):
            cnt+=1     
    if cnt==len(J):
        flag=1
    else:
        if cnt!=0:
            flag=len(J)+1
        else:
            flag=cnt                    
    
    last=len(Holder)
    
    Info=[]
    ops=[]
    if 'where' in Holder:
        last=Holder.index('where')
        St=''
        for i in range(last+1,len(Holder)):
            St+=Holder[i]    
        Info,ops=Where_Handler(St,Dict)
        # print(Info)   
        if Info==-1 or ops==-1:
            return     
    #list all error possibilities    
    if last<pos_from:
        print("ERROR: WRONG QUERY FORMAT")    
        
    else:
        if S=='*':
            Type1(Holder[pos_from+1:last],Dict,begin-1,Info,ops)
        else:
            if flag==0:
                # print(Holder[pos_from+1:last],S,Dict,begin-1,Info,ops)
                Type2(Holder[pos_from+1:last],S,Dict,begin-1,Info,ops)
            if flag==1:
                Type3(Holder[pos_from+1:last],J,Dict,begin-1,Info,ops)
            if flag>=2:
                print("ERROR: WRONG USE OF AGGREGATE QUERIES")


def JoinTable(T1,T2,label1,label2):
    T3=[]
    for i in range(len(T2)):
        for j in range(len(T1)):
            x=T1[j].copy()
            for k in range(len(T2[i])):
                x.append(T2[i][k])
            T3.append(x)    
    label3=label1
    for it in label2:
        label3.append(it)        
    return T3,label3        


if __name__ == "__main__":
    Meta=Meta_Read()
    ReadAll(Meta)
    Query(str(sys.argv[1]),Meta)
