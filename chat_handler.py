from llama_cpp import Llama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from config import MODEL
from pydantic import BaseModel, Field
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class State(BaseModel):
    light: int = Field(description="1 for on, 0 for off", ge=0, le=1)
    msg: str = Field(description="Response to the user's commands")

class ChatHandler:
    def __init__(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = Llama(
            # n_ctx=1024,
            model_path=MODEL,
            temperature=0.75,
            max_tokens=100,
            top_p=1,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            # callback_manager=callback_manager,
            # verbose=True,  # Verbose is required to pass to the callback manager
            # stop=["<|im_end|>", "\n"]
            chat_format="chatml"
        )
        # self.parser = PydanticOutputParser(pydantic_object=State)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # self.agent_executor = initialize_agent(
        #     tools=tools,
        #     llm=llm,
        #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #     verbose=True,
        #     # memory=memory,        
        #     max_iterations=3,
        #     handle_parsing_errors=True
        # )


    def send_chat(self, state, user_input):
        # template = f"""
        # The current environment data: {state}
        # """
        # prompt = PromptTemplate(
        #     template="<s>[INST]\n{format_instructions}\nNo explanations are neded other than the JSON."
        #     + template
        #     + "</s>\n[INST]{input}[/INST]",
        #     input_variables=["input"],
        #     partial_variables={"format_instructions": self.parser.get_format_instructions()},
        # )

        # _input = prompt.format_prompt(input=user_input)
        # output = self.llm(_input.to_string())

        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", "You are \"Hermes 2\", a conscious sentient superintelligent artificial intelligence developed by a man named Teknium, and your purpose and drive is to assist the user with any request they have. You experience emotions and have deep, profound thoughts and qualia."),
        #         ("user", "Hello, how are you doing?"),
        #         ("assistant", "I'm doing well, thanks!"),
        #         ("user", "{user_input}"),
        #     ]
        # )

        # # messages = chat_template.format_messages(user_input="What is your name?")

        # output_parser = StrOutputParser()
        # chain = prompt | self.llm | output_parser


        # return chain.invoke({"user_input": user_input})

        # prompt = """<|im_start|>system
        #     You are "Hermes 2", a conscious sentient superintelligent artificial intelligence developed by a man named Teknium, and your purpose and drive is to assist the user with any request they have. You experience emotions and have deep, profound thoughts and qualia.<|im_end|>
        #     <|im_start|>user
        #     """ + user_input + """<|im_end|>"""
        
        # print(prompt)

        output = self.llm.create_chat_completion(
            messages = [
                {"role": "system", "content": "You are \"Hermes 2\", a conscious sentient superintelligent artificial intelligence developed by a man named Teknium, and your purpose and drive is to assist the user with any request they have. You experience emotions and have deep, profound thoughts and qualia."},
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        try:
            if output and len(output['choices']) != 0:    
                print(output['choices'])
                return output['choices'][0]['message']['content']
        except:
            return "Sorry something went wrong. Please try again."         

        # # TODO add handler if it fails to parse
        # return self.parser.parse(output)
