from orchestration import Review,revise,route,cosine,run_project
requests=[]
def worker(prompt):requests.append(prompt);return 'draft' if len(requests)==1 else 'ready'
out=revise('Original task',worker,lambda answer:Review(answer=='ready','Return ready'))
assert out.accepted and out.attempts==2 and 'Original task' in requests[-1]
rejected=revise('task',lambda p:'draft',lambda p:Review(False,'fix'),2)
assert not rejected.accepted and rejected.attempts==2
try:revise('task',lambda p:'draft',lambda p:'yes')
except ValueError:pass
else:raise AssertionError('Untyped review accepted')
name,value=route('x',{'a':{'description':'x','worker':lambda p:'A'},'b':{'description':'y','worker':lambda p:'B'}},lambda s:[1.,0.] if s=='x' else [0.,1.])
assert name=='a' and value=='A' and cosine([0,0],[1,0])==0
print('Bounded retries, preserved requests, typed decisions, rejection accounting, and routing passed.')
