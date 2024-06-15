import {Button, Flex, Icon, Text, Textarea, useColorModeValue} from "@chakra-ui/react"
import {useMutation, useQueryClient} from "@tanstack/react-query"
import {createFileRoute, SearchSchemaInput} from "@tanstack/react-router"
import {ChatService, CnvMessageUserCreateFront, ConversationsService} from "../../client";
import React, {RefObject, useEffect, useRef, useState} from "react";
import {MdAutoAwesome, MdPerson} from "react-icons/md";
import {z} from "zod";

export const Route = createFileRoute("/_layout/")({
    component: Dashboard,
    validateSearch: (
        input: {
          conversation_id?: number
        } & SearchSchemaInput,
    ) =>
        z.object({
              conversation_id: z.number().catch(NaN)
            }).parse(input),
})

function ChatMessage(props: { message: CnvMessageUserCreateFront, key?: number }) {
    const {message} = props
    const borderColor = useColorModeValue('gray.200', 'whiteAlpha.200');
    const brandColor = useColorModeValue('brand.500', 'white');
    const textColor = useColorModeValue('navy.700', 'white');

    return (
        <Flex key={message.id} w="100%" align={'center'} mb="10px">
            {message.role === 'user' ?
                <Flex
                    borderRadius="full"
                    justify="center"
                    align="center"
                    bg={'transparent'}
                    border="1px solid"
                    borderColor={borderColor}
                    me="20px"
                    h="40px"
                    minH="40px"
                    minW="40px"
                >
                    <Icon
                        as={MdPerson}
                        width="20px"
                        height="20px"
                        color={brandColor}
                    />
                </Flex>
                :
                <Flex
                    borderRadius="full"
                    justify="center"
                    align="center"
                    bg={'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%)'}
                    me="20px"
                    h="40px"
                    minH="40px"
                    minW="40px"
                >
                    <Icon
                        as={MdAutoAwesome}
                        width="20px"
                        height="20px"
                        color="white"
                    />
                </Flex>}
            <Flex
                p="22px"
                border="1px solid"
                borderColor={borderColor}
                borderRadius="14px"
                w="100%"
                zIndex={'2'}
            >
                <Text
                    color={textColor}
                    fontWeight="600"
                    fontSize={{base: 'sm', md: 'md'}}
                    lineHeight={{base: '24px', md: '26px'}}
                >
                    {message.content}
                </Text>
            </Flex>

        </Flex>
    )

}
interface ChatInputProps {
    handleTranslate: (inputText: string) => void; // Adjust the parameter and return type as needed
    handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void; // Adjust the parameter type as needed
    endOfPageRef: React.RefObject<HTMLButtonElement>; // Adjust the type if it's a different kind of ref
    loading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({handleTranslate, handleChange, endOfPageRef, loading}) => {
    const [value, setValue] = useState<string>('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const borderColor = useColorModeValue('gray.200', 'whiteAlpha.200');
    const inputColor = useColorModeValue('navy.700', 'white');
    const placeholderColor = useColorModeValue(
        {color: 'gray.500'},
        {color: 'whiteAlpha.600'},
    );
    const handleResize = () => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        }

    };
    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            handleResize();
        }
    }, [value]);
    const handleKeyDown = (Event: any) => {
      if (Event.ctrlKey && Event.key === 'Enter') {
          return handleOnClick();
      }
    };
    const handleInputChange = (Event: any) => {
        setValue(Event.target.value);
        handleChange(Event);
    }

    const handleOnClick = () => {
        const maxCodeLength = 700;
        if (!value) {
            alert('Please enter your message.');
            return;
        }
        if (value.length > maxCodeLength) {
            alert(
                `Please enter code less than ${maxCodeLength} characters. You are currently at ${value.length} characters.`,
            );
            return;
        }
        handleTranslate(value);
        setValue('');
        handleResize();
    };

    return (
        <Flex
            ms={{base: '0px', xl: '60px'}}
            mt="20px"
            justifySelf={'flex-end'}
        >
            <Textarea
                value={value}
                ref={textareaRef}
                onInput={handleResize}
                overflow="hidden"
                resize="none"
                minH="54px"
                h="100%"
                border="1px solid"
                borderColor={borderColor}
                borderRadius="45px"
                p="15px 20px"
                me="10px"
                fontSize="sm"
                fontWeight="500"
                _focus={{borderColor: 'none'}}
                color={inputColor}
                _placeholder={placeholderColor}
                placeholder="Type your message here..."
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
            />
            <Button
                ref={endOfPageRef}
                variant="primary"
                py="20px"
                px="16px"
                fontSize="sm"
                borderRadius="45px"
                ms="auto"
                w={{base: '160px', md: '210px'}}
                h="54px"
                _hover={{
                    boxShadow:
                        '0px 21px 27px -10px rgba(96, 60, 255, 0.48) !important',
                    bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%) !important',
                    _disabled: {
                        bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%)',
                    },
                }}
                onClick={handleOnClick}
                isLoading={loading ? true : false}
            >
                Submit
            </Button>

        </Flex>
    )
}

function Dashboard() {
    const { conversation_id } = Route.useSearch()
    const queryClient = useQueryClient()
    const [messages, setMessages] = useState<CnvMessageUserCreateFront[]>([])
    const [inputCode, setInputCode] = useState<string>('');
    const [outputCode, setOutputCode] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [loadingConversation, setLoadingConversation] = useState(true)
    const [conversationId, setConversationId] = useState<number>(NaN);

    const endOfPageRef: RefObject<HTMLButtonElement> = useRef<HTMLButtonElement>(null);


    const addMessage = (newMessage: CnvMessageUserCreateFront) => {
        let foundObject = messages.find(obj => obj.id === newMessage.id);
        if (!foundObject) {
            setMessages(prevMessages => [...prevMessages, newMessage]);
        }
    };

    const handleChange = (Event: any) => {
        setInputCode(Event.target.value);
    };

    const scrollToTheEnd = () => {
        setTimeout(() => {
            if (endOfPageRef.current) {
                endOfPageRef.current.scrollIntoView({behavior: 'smooth'});
            }
        }, 500);
    }
    const readConversation = async (conversation_id: number) => {
        const response = await ConversationsService.readConversation({id: conversation_id})
        response.messages.forEach(msg => addMessage(msg))// This will run if the promise is resolved
    }

    const sendChatMessage = async (content: string) => {
        if (conversationId) {
            const response = await ChatService.chatContinueConversation({
                conversationId: conversationId, requestBody: {content}
            })
            addMessage({role: 'user', content: content, id: response.question_id})
            addMessage({role: 'assistant', content: response.content, id: response.answer_id})
            scrollToTheEnd()
        } else {
            const response = await ChatService.chatNewConversation({
                requestBody: {content}
            })
            addMessage({role: 'user', content: content, id: response.question_id})
            addMessage({role: 'assistant', content: response.content, id: response.answer_id})
            setConversationId(response.conversation_id)
            scrollToTheEnd()
        }
    }

    const chatMutation = useMutation({
        mutationFn: sendChatMessage,
        onSuccess: () => {
            setLoading(false);
        },
        onError: () => {
            // TODO handle error
            setLoading(false);
        },
        onSettled: () => {
            queryClient.invalidateQueries({
                queryKey: ["chat"],
            })
        },
    })

    const conversationMutation = useMutation({
        mutationFn: readConversation,
        onSuccess: () => {
            setLoadingConversation(false);
        },
        onError: () => {
            // TODO handle error
            setLoading(false);
        },
        onSettled: () => {
            queryClient.invalidateQueries({
                queryKey: ["conversations"],
            })
        },
    })

    const handleTranslate = async (textInput: string) => {
        console.log(textInput);
        setInputCode(textInput);
        setOutputCode(' ');
        setLoading(true);
        chatMutation.mutate(inputCode);
    };

    if (loadingConversation && conversation_id) {
        conversationMutation.mutate(conversation_id)
        setOutputCode(' ');
        setLoadingConversation(false)
        setConversationId(conversation_id)
        scrollToTheEnd()
    }
    return (
        <>
            <Flex
                w="100%"
                pt={{base: '70px', md: '0px'}}
                direction="column"
                position="relative"
            >
                <Flex
                    direction="column"
                    mx="auto"
                    w={{base: '100%', md: '100%', xl: '100%'}}
                    minH={{base: '75vh', '2xl': '85vh'}}
                    maxW="1000px"
                >

                    <Flex direction={'column'} w="100%" mb={outputCode ? '20px' : 'auto'}>
                    </Flex>
                    <Flex
                        direction="column"
                        w="100%"
                        mx="auto"
                        display={outputCode ? 'flex' : 'none'}
                        mb={'auto'}
                    >
                        {messages.map(message =>
                            <ChatMessage key={message.id} message={message}></ChatMessage>
                        )}

                    </Flex>
                    <ChatInput
                        handleTranslate={handleTranslate}
                        endOfPageRef={endOfPageRef}
                        handleChange={handleChange}
                        loading={loading}
                    ></ChatInput>

                    <Flex
                        ms={{base: '0px', xl: '60px'}}
                        mt="20px"
                        justifySelf={'flex-end'}>
                    </Flex>
                </Flex>
            </Flex>

        </>
    )
}
