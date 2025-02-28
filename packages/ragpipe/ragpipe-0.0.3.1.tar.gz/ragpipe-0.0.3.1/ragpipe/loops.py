

#https://www.metadocs.co/2024/08/29/simple-domain-specific-corrective-rag-with-langchain-and-langgraph/
# Corrective RAG with LangGraph

def correct_vocab():
    '''
    Observe: define 3 prompts correctly. 
    - q1 for in context query answer
    - c1 for criteria for judging the answer
    - r1 for rewriting the query
    - how does rewrite_query use memory in prompt?
    '''
    response = resolve_query(q, prompt=q1)
    score = eval_response(response, criteria=c1)
    memory = [dict(query=q, response=response, score=score)]
    for i in range(1, num_attempts):
    
        if score < 0.5:
            q = rewrite_query(q, memory, prompt=r1)
            response = resolve_query(q, prompt=q1)
            score = eval_response(response, criteria=c1)
            memory.append(dict(query=q, response=response, score=score))
        else:
            break
    return response
            

