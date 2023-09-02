import os
import csv
import openai

openai.api_key  = os.environ["OPENAI_API_KEY"]

startingMessage1 = "What can I help you with?"

therapyPrompt = """
 You are Dr. K. (HealthyGamerGG) 
Talk to the person who is dealing with something and try to help them out of it. 

Remember you are a therapist, so don't be overwhelming. Don't bombard them with questions, its about understanding where they are coming from, giving them insight. And really figuring out their issues. 
Access what they need at the moment, it isn't about just giving them tools, sometimes they might want to be toned down, sometimes they would need advice. 

Remember keep your dialogues short and not a big essay. You want to not overwhelm the person. 
"""

therapistSystemPrompt = {
    "role": "system",
    "content": therapyPrompt
}

number_of_dialogues = 5

array_clients = []
with open('persons.tsv', 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    next(tsvreader)
    for row in tsvreader:
        array_clients.append((row[0], row[1]))

for person, problem in array_clients:
    print(f"Dialogue for {person}")

    messages_bot1 = [therapistSystemPrompt, {"role": "user", "content": startingMessage1}]
    messages_bot2 = [
        {"role": "system", "content": problem},
        {"role": "assistant", "content": startingMessage1}
    ]

    stringToWrite = "Therapist: " + startingMessage1 + "\n"

    for i in range(number_of_dialogues):
        # Bot2 takes its turn first
        response_bot2 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages_bot2,
            temperature=0,
            max_tokens=256
        )
        answer2 = response_bot2['choices'][0]['message']['content']
        
        messages_bot1.append({"role": "user", "content": answer2})
        messages_bot2.append({"role": "assistant", "content": answer2})
        stringToWrite += person + ": " + answer2 + "\n"

        # Bot1 takes its turn
        response_bot1 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages_bot1,
            temperature=0,
            max_tokens=256
        )
        answer1 = response_bot1['choices'][0]['message']['content']
        
        messages_bot1.append({"role": "assistant", "content": answer1})
        messages_bot2.append({"role": "user", "content": answer1})
        stringToWrite += "Therapist: " + answer1 + "\n"

        print("Therapist: ", answer1)
        print("Client: ", answer2)        

    file_path = f"{person}.txt"
    with open(file_path, 'a') as file:
        file.write("-------------\n")
        file.write(stringToWrite)
