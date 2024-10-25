from llm_response.langgraph_graph_state import GraphState
from prompt.final_selecting_for_recomm import FINAL_SELECTING_FOR_RECOMM, FINAL_SELECTING_FOR_RECOMM_v2

def final_selecting_for_recomm(llm, state: GraphState):
   print("Final formatting for recomm".ljust(100, '-'))
   print("state['query'] : ", {state['query']})
   print("state['intent'] : ", {',\n'.join(state['intent'])})
   print("(state['candidate_str'] : ", {state['candidate_str']})
   prompt = FINAL_SELECTING_FOR_RECOMM_v2.format(
      query=state['query'], 
      intent=',\n'.join(state['intent']),
      candidates=state['candidate_str']
   )
   print(f"prompt : {prompt}")
   response = llm.invoke(prompt)
   print(response.content)
   print(f"input tokens : {response.usage_metadata['input_tokens']:,}")
   state['selected_recommendations'] = eval(response.content.replace('```', '').replace('json', '').strip())
   return state