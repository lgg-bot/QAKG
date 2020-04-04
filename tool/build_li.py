html=""
html+="<ul>\n"
f=open('../dict/symptoms.txt','r')
n=217
for i in f:
    html+='<li class="second-menu"><a href="/deal_request?name={}&id={}" id="{}">{}</a></li>\n'.format(i.strip(),n,n,i.strip())
    n+=1
html+="</ul>"
print(html)
