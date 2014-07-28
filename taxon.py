#!/usr/bin/python3
import sqlite3

def Create():
    Id=dict()
    Data=list()
    Name=dict()
    Specie=list()
    Son=dict()
    GreatSon=dict()
    Parent=dict()
    Rank=dict()
    global Taxon
    Taxon=list()
    with open('./test/name','r') as In:
        Raw=list(In.readlines())
        for record in Raw:
            add=record.replace('\n','').split(sep='|')
            if add[0] not in Name or add[3]=='scientific name':
                Name[add[0]]=add[1]
    with open('./test/nodes','r') as In:
        Raw=list(In.readlines())
        for record in Raw:
            add=record.replace('\n','').split(sep=' ')
            Id[add[0]]=add[1]
            Rank[add[0]]=add[2]
            if add[2]=='species':
                Specie.append(add[0])
    for specie in Specie:
        record=[specie,]
        while Id[specie]!='1' :
            record.append(Id[specie])
            specie=Id[specie]
#        if '33090' in record:
#            record.pop()
#            record.pop()
            Data.append(record)
    for data in Data:
        for n in range(len(data)):
            if data[n] not in Parent:
                Parent[data[n]]=data[(n+1):]
            if n==0:
                continue
            if data[n] not in Son:
                Son[data[n]]={data[n-1],}
            else:
                Son[data[n]].add(data[n-1])
            if data[n] not in GreatSon:
                GreatSon[data[n]]={data[0],}
            else:
                GreatSon[data[n]].add(data[0])
    for specie in Name.items():
        if specie[0] not in Son:
            Son[specie[0]]=set()
        if specie[0] not in Parent:
            Parent[specie[0]]=list()
        record=[specie[0],Name[specie[0]],Rank[specie[0]],Son[specie[0]],Parent[specie[0]],GreatSon[specie[0]]]
        Taxon.append(record)
    return


def Database():
    con=sqlite3.connect('./test/DB')
    cur=con.cursor()
    cur.execute('create table if not exists taxon (Id text,Name text,Rank text,Son text,Parent text,GreatSon text);')
    for line in Taxon:
        Son=' '.join(line[3])
#        Parent=str(line[4])
        Parent=' '.join(line[4])
        GreatSon=' '.join(line[5])
        cur.execute('insert into taxon (Id,Name,Rank,Son,Parent,GreatSon) values (?,?,?,?,?,?);',(line[0],line[1],line[2],Son,Parent,GreatSon))
    con.commit()
    cur.close()
    con.close()
    print('Done.\n')
    return
    
def Query():
    while True:
        Querytype=input('1.by id\n2.by name\n')
        if Querytype not in ['1','2']:
            return
        con=sqlite3.connect('./test/DB')
        cur=con.cursor()
        if Querytype=='1':
            Id=input('taxon id:\n')
            cur.execute('select * from taxon where Id=?;',(Id,))
            Result=cur.fetchall()
        elif Querytype=='2':
            Name=input('scientific name:\n')
            cur.execute('select * from taxon where Name like ?;',('%'+Name+'%',))
            Result=cur.fetchall()
        cur.close()
        con.close()
        for i in Result:
            Id=i[0]
            Name=i[1]
            Rank=i[2]
            Son=i[3].split(sep=' ')
            Parent=i[4].split(sep=' ')
            GreatSon=i[5].split(sep=' ')
            print('id      : ',Id,'\n')
            print('name    : ',Name,'\n')
            print('rank    : ',Rank,'\n')
            print('parent  : ','->'.join(Parent),'\n')
            print('son     : ',','.join(Son),'\n')
            print('greatson: ',','.join(GreatSon),'\n\n')

work=input('1.Init database\n2.query\n')
if work not in ['1','2']:
    raise ValueError('wrong input!\n')
if work=='1':
    Create()
    Database()
elif work=='2':
    Query()
