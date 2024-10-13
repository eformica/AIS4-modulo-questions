# from nomic.gpt4all import GPT4All
 
# # Inicialize o modelo GPT4All
# m = GPT4All()
# m.open()
 
# # Gere uma resposta com base em um estímulo
# response = m.prompt('escreva uma história sobre um computador solitário')
 
# # Imprime a resposta gerada
# print(response)

from gpt4all import GPT4All
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf") # downloads / loads a 4.66GB LLM

with model.chat_session():
    print(model.generate("Liste os planetas do sistema solar, de forma estruturada em JSON com uma breve ficha técnica de cada um."))