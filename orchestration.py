"""Provider-neutral routing and bounded evaluation workflows."""
import math
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Review:
    passed:bool
    feedback:str=''

@dataclass(frozen=True)
class Outcome:
    response:str
    accepted:bool
    attempts:int
    history:tuple

def revise(request,worker:Callable[[str],str],reviewer:Callable[[str],Review],max_attempts=3):
    if type(max_attempts) is not int or max_attempts<1:raise ValueError('Positive attempt budget required')
    prompt=request;history=[]
    for attempt in range(1,max_attempts+1):
        response=str(worker(prompt));review=reviewer(response)
        if not isinstance(review,Review) or type(review.passed) is not bool:raise ValueError('Reviewer must return a Review with a boolean decision')
        history.append({'attempt':attempt,'response':response,'accepted':review.passed,'feedback':review.feedback})
        if review.passed:return Outcome(response,True,attempt,tuple(history))
        prompt=f'Original request: {request}\nPrevious response: {response}\nRequired correction: {review.feedback}\nReturn the complete revised result.'
    return Outcome(response,False,max_attempts,tuple(history))

def cosine(a,b):
    a,b=list(a),list(b)
    if not a or len(a)!=len(b) or not all(math.isfinite(x) for x in a+b):raise ValueError('Aligned finite embedding vectors required')
    norm=math.sqrt(sum(x*x for x in a))*math.sqrt(sum(x*x for x in b))
    return sum(x*y for x,y in zip(a,b))/norm if norm else 0.

def route(request,routes,embed):
    if not routes:raise ValueError('At least one named route is required')
    query=embed(request)
    selected=max(routes,key=lambda name:cosine(query,embed(routes[name]['description'])))
    return selected,routes[selected]['worker'](request)

def run_project(brief,workers,reviewers):
    """Produce reviewed stories, features, then tasks; stop on any failed gate."""
    artifacts={}
    for stage in ('stories','features','tasks'):
        prompt=brief+'\nPrior reviewed artifacts: '+repr(artifacts)
        outcome=revise(prompt,workers[stage],reviewers[stage])
        artifacts[stage]=outcome
        if not outcome.accepted:break
    return artifacts
