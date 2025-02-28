from pydantic import BaseModel
from openai import OpenAI
import json

class AuthenticityResponse(BaseModel):
    correct: bool
    reason: str

def judge_authenticity(correct_output_description: str, output_to_judge: str):
    client = OpenAI()
    system_message = f"""
    You are a helpful assistant that judges the authenticity of the output. 
    You should judge the authenticity of the output following the description.
    You should return a JSON object that has a correct key and a reason key.
    Correct output description: 
    {correct_output_description}
    
    Output to judge: 
    {output_to_judge}
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message}],
        response_format=AuthenticityResponse   
    )
    dict_response = json.loads(response.choices[0].message.content) # type: ignore
    correct = dict_response["correct"]
    reason = dict_response["reason"]
    return correct, reason

if __name__ == "__main__":
    correct, reason = judge_authenticity("keyがtestでvalueがstr型のJSONformat", '{"test": "test"}')  # エスケープシーケンスを修正
    print(correct)
    print(reason)
    print(type(correct))
    print(type(reason))
