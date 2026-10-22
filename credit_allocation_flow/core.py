from collections import deque
from .common import integer,identifier,unique_ids

def run(data):
    lines=data['invoice_lines'];credits=data['credits']
    if len(lines)>100 or len(credits)>100:raise ValueError('size')
    unique_ids(lines);unique_ids(credits);known={r['id']:i for i,r in enumerate(lines)};N=2+len(lines)+len(credits);source=N-2;sink=N-1;graph=[[] for _ in range(N)]
    def add(a,b,capacity):
        edge=[b,len(graph[b]),capacity,capacity];rev=[a,len(graph[a]),0,0];graph[a].append(edge);graph[b].append(rev);return edge
    for i,line in enumerate(lines):
        integer(line['remaining_cents'],0,10**12);identifier(line['currency']);identifier(line['vat_code']);add(len(credits)+i,sink,line['remaining_cents'])
    tracked=[];rejected=[];source_edges=[]
    for i,c in enumerate(credits):
        amount=integer(c['amount_cents'],0,10**12);identifier(c['currency']);identifier(c['vat_code']);source_edges.append(add(source,i,amount))
        eligible=c['eligible_lines']
        if len(eligible)!=len(set(eligible)) or not set(eligible)<=set(known):raise ValueError('eligibility')
        for key in eligible:
            j=known[key];line=lines[j]
            if any(c[k]!=line[k] for k in ('currency','vat_code')):rejected.append({'credit':c['id'],'line':key,'reason':'currency_or_vat_mismatch'});continue
            tracked.append((c['id'],key,add(i,len(credits)+j,amount)))
    total=0
    while True:
        levels=[-1]*N;levels[source]=0;queue=deque([source])
        while queue:
            a=queue.popleft()
            for b,_,capacity,_ in graph[a]:
                if capacity and levels[b]<0:levels[b]=levels[a]+1;queue.append(b)
        if levels[sink]<0:break
        cursor=[0]*N
        def send(a,amount):
            if a==sink:return amount
            while cursor[a]<len(graph[a]):
                e=graph[a][cursor[a]];b,reverse,capacity,_=e
                if capacity and levels[b]==levels[a]+1:
                    pushed=send(b,min(amount,capacity))
                    if pushed:e[2]-=pushed;graph[b][reverse][2]+=pushed;return pushed
                cursor[a]+=1
            return 0
        while True:
            pushed=send(source,10**18)
            if not pushed:break
            total+=pushed
    currencies={c['id']:c['currency'] for c in credits};totals={}
    for credit,_,edge in tracked:
        if edge[2]<edge[3]:totals[currencies[credit]]=totals.get(currencies[credit],0)+edge[3]-edge[2]
    return {'fully_allocated':all(e[2]==0 for e in source_edges),'allocated_cents':total if len(totals)<=1 else None,'allocated_cents_by_currency':totals,'allocations':[{'credit':a,'line':b,'cents':e[3]-e[2]} for a,b,e in tracked if e[2]<e[3]],'unallocated':[{'credit':c['id'],'cents':edge[2]} for c,edge in zip(credits,source_edges) if edge[2]],'rejected_eligibility_edges':rejected,'scope':'declared currency/VAT/remaining capacities; no bookkeeping or payment execution'}
