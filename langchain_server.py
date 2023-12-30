from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory

qa: ConversationalRetrievalChain = None


def update_qa(retriever):
    global qa

    llm = ChatOpenAI(model_name="gpt-4-1106-preview")
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)


def request_llm(question):
    global qa

    result = qa(question)
    return result["answer"]

