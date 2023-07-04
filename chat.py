import asyncio
import streamlit as st
from sydney import SydneyClient
import os
from streamlit_chat import message

st.set_page_config(page_title="Chat", page_icon="🤖")
key = os.environ.get("key_bing2023")

method = st.selectbox("Elige un método", ("Chat", "Creativo"))

if method == "Creativo":
    crea = st.selectbox("Elige un tipo", ("Ideas", "Email", "Párrafo"))

if method == "Chat":
    st.title('Chat 🤖')
elif method == "Creativo":
    st.title('Crear 📝')



if method == "ask_stream":
    st.title('Chat 🤖')
elif method == "compose_stream":
    st.title('Crear 📝')



def user_input():
    prompt = st.text_input('Coloque su prompt aqui: ', key="user_input")
    return prompt

async def response_api(prompt: str) -> str:
    async with SydneyClient() as sydney:
        response_text = ""
        if method == "Chat":
            async for response in sydney.ask_stream(prompt):
                response_text += response
        elif method == "Creativo":
            if crea == "Ideas":
                async for response in sydney.compose_stream(prompt, format="ideas"):
                    response_text += response
            elif crea == "Email":
                async for response in sydney.compose_stream(prompt, format="email"):
                    response_text += response
            elif crea == "Párrafo":
                async for response in sydney.compose_stream(prompt, format="paragraph"):
                    response_text += response
        return response_text

async def main():
    if 'generate' not in st.session_state:
        st.session_state['generate'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []



    user_text = user_input()

    if user_text:
        output = await response_api(user_text)
        st.session_state.generate.append(output)
        st.session_state.past.append(user_text)

    if st.session_state['generate']:
        for i in range(len(st.session_state['generate'])-1,-1,-1):
            message(st.session_state["past"][i], is_user=True, key=f"{i}_user")
            message(st.session_state["generate"][i], key=f"{i}")


if __name__ == "__main__":
    asyncio.run(main())
