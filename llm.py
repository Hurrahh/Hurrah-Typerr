from huggingface_hub import InferenceClient


token = "" # Your Hugging Face Token


def llm(text,mode):
    client = InferenceClient(token=token)

    if mode == 'quiz':
        messages = [
            {
                "role": "user",
                "content": text + "This is the mcq question with 4 options. Just output the numerical option 1,2,3,4, nothing else"
            }
        ]
    else:
        messages = [
            {
                "role": "user",
                "content": text + "Write c++ code without comments"
            }
        ]

    #
    # response = model.invoke(messages)
    # # return response
    # print(response)

    completion = client.chat_completion(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        temperature=0.5,
        max_tokens=2048,
        top_p=0.7
    )
    print("Answer processed")
    print(completion.choices[0].message.content)

    return completion.choices[0].message.content

# llm('binary tree')