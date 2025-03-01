from openai import OpenAI

def consult_with_deepchat(base_url,api_key,model,user_msg,system_msg):

    openai = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    stream = True # or False

    chat_completion = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        stream=stream,
    )

    OUT='';
    if stream:
        for event in chat_completion:
            if event.choices[0].finish_reason:
                pass
                #print(event.choices[0].finish_reason,
                #      event.usage.prompt_tokens,
                #      event.usage.completion_tokens)
            else:
                OUT=OUT+event.choices[0].delta.content
    #else:
    #    print(chat_completion.choices[0].message.content)
    #    print(chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens)


    return OUT
