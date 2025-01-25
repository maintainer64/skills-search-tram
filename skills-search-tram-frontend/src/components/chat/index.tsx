'use client'
import {css} from '@emotion/css';
import {ChatMessageProps, ChatProps} from "@/components/chat/types";
import {AliceIcon} from "./alice-icon";
import {YandexConversationIcon} from "./conversation-icon";
import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {rangeP, mapP} from "@/components/parallax-providers/map-scroll-effect";

const styles = {
    container: css`
        background-color: #f9f9f9;
        padding: 20px;
        margin: 0 auto;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        flex-direction: column;
    `,
    icon: css`
        justify-content: center;
        padding-right: 0;
        width: 64px;
        height: 64px;
        flex-shrink: 0;
        margin: auto;
    `,
    date: css`
        text-align: center;
        color: #888;
        margin: 0 auto;
        padding: 30px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        font-size: 14px;
    `,
    messageContainer: css`
        position: relative;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 8px;
        align-self: end;
    `,
    userMessage: css`
        margin-left: 48px;
        background-color: #fff;
        margin-bottom: 10px;
        text-align: left;
        max-width: 70%;
        align-self: flex-end;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        font-weight: 400;
        border-radius: 24px 4px 24px 24px;
        padding: 10px 16px;
    `,
    botMessage: css`
        margin-bottom: 10px;
        text-align: left;
        max-width: 70%;
        align-self: flex-start;
        font-weight: 400;
        padding: 10px 16px;
    `
};


export function YandexMessage({message, index, messages}: {
    message: ChatMessageProps,
    index: number,
    messages: ChatMessageProps[]
}) {
    const {chatBlock: {progress}} = useHomeParallaxContext();
    const max = 0.7;
    const opacity = rangeP(
        index * max / messages.length,
        (index + 1) * max / messages.length,
        progress
    );
    const translate = mapP(50, 0, opacity);
    return <div key={index} className={styles.messageContainer}>
        <div style={{
            opacity: opacity,
            transform: `translateY(${translate}%)`
        }} className={message.bot ? styles.botMessage : styles.userMessage}>
            {message.text}
        </div>
    </div>
}

export function YandexChat({date, messages}: ChatProps) {
    const {chatBlock: {progress}} = useHomeParallaxContext();
    return (
        <div style={{
            maxWidth: `${mapP(80, 101, progress)}%`,
        }}
             className={styles.container}>
            <div className={styles.date}><YandexConversationIcon/>{date}</div>
            {messages.map((message, index, messages) => (
                <YandexMessage key={index} message={message} index={index} messages={messages}/>
            ))}
            <div className={styles.messageContainer}>
                <div className={styles.icon}>
                    <AliceIcon/>
                </div>
            </div>
        </div>
    );
}

export default YandexChat;
