from fastapi import HTTPException
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic.v1.types import SecretStr
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.exception import ApiDbException
from app.models import CnvMessage, CnvMessageAssistantCreate, Conversation


class SystemPrompts:
    summary_generator: str = "Podsumuj konwersacje w 5 słowach"
    assistant: str = "Jesteś pomocnym asystentem"


class StaticAnswers:
    mock_ans: str = "Mock answer"
    mock_summary: str = "Mock summary"
    unsafe_mes: str = "Hola, hola... jestem od tego żeby Ci pomóc się uczyć także zważaj na słowa i na to o co pytasz."


class OpenAIModels:
    gpt_35_turbo = "gpt-3.5-turbo"


class LLMController:
    def __init__(self) -> None:
        self.openai_client = OpenAI(api_key=settings.OPEN_API_KEY)
        self.chat_open_ai = ChatOpenAI(api_key=SecretStr(settings.OPEN_API_KEY))
        self.str_output_parser = StrOutputParser()

    def moderate_input_is_flagged(self, text_to_validate: str) -> bool:
        response = self.openai_client.moderations.create(input=text_to_validate)
        output = response.results[0]
        return output.flagged

    def single_completion(
        self,
        system_input: str,
        messages_list: list[CnvMessage],
        model: str = OpenAIModels.gpt_35_turbo,
        max_tokens: int = 2000,
    ) -> str | None:
        typed_messages: list[
            ChatCompletionSystemMessageParam
            | ChatCompletionUserMessageParam
            | ChatCompletionAssistantMessageParam
        ] = []
        for msg in messages_list:
            if msg.role == "user":
                typed_messages.append(
                    ChatCompletionUserMessageParam(role="user", content=msg.content)
                )
            elif msg.role == "assistant":
                typed_messages.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant", content=msg.content
                    )
                )
        system_message = ChatCompletionSystemMessageParam(
            role="system", content=system_input
        )
        typed_messages.insert(0, system_message)
        chat_completion = self.openai_client.chat.completions.create(
            model=model, max_tokens=max_tokens, messages=typed_messages
        )
        return chat_completion.choices[0].message.content


def generate_answer(*, session: Session, owner_id: int, conv_id: int) -> CnvMessage:
    conversation = session.get(Conversation, conv_id)
    if not conversation or conversation.id is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.id is None:
        raise ApiDbException("Conversation without id")
    if settings.AI_MOCK_REST_CALLS:
        return crud.create_cnvmessage(
            session=session,
            cnv_in=CnvMessageAssistantCreate(content=StaticAnswers.mock_ans),
            owner_id=owner_id,
            conv_id=conversation.id,
        )
    llm = LLMController()
    is_flagged = llm.moderate_input_is_flagged(conversation.messages[-1].content)
    if is_flagged:
        return crud.create_cnvmessage(
            session=session,
            cnv_in=CnvMessageAssistantCreate(content=StaticAnswers.unsafe_mes),
            owner_id=owner_id,
            conv_id=conversation.id,
        )
    generated_answer = llm.single_completion(
        system_input=SystemPrompts.assistant, messages_list=conversation.messages
    )
    assistant_msg = CnvMessageAssistantCreate(content=generated_answer)
    return crud.create_cnvmessage(
        session=session,
        cnv_in=assistant_msg,
        owner_id=owner_id,
        conv_id=conversation.id,
    )


def generate_summary(*, session: Session, conv_id: int) -> str | None:
    conversation = session.get(Conversation, conv_id)
    if not conversation or conversation.id is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.id is None:
        raise ApiDbException("Conversation without id")
    if settings.AI_MOCK_REST_CALLS:
        return StaticAnswers.mock_summary
    llm = LLMController()
    return llm.single_completion(
        system_input=SystemPrompts.summary_generator,
        messages_list=conversation.messages,
        max_tokens=20,
    )
