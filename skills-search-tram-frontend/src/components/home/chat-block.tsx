'use client'


import YandexChat from "@/components/chat";
import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {getConversation, conversations} from "@/components/meta";
import {css} from "@emotion/css";
import {mapP, rangeP} from "@/components/parallax-providers/map-scroll-effect";

const styles = {
    container: css`
        display: block;
        position: relative;
        height: inherit;
    `,
    header: css`
        padding: 0 0 10pt 0;
    `
}

export function HeaderChatBlock() {
    const {chatBlock: {progress}} = useHomeParallaxContext();
    const animation = {
        opacity: rangeP(
            0,
            0.4,
            progress
        ),
        paddingTop: `${mapP(40, 200, progress)}pt`,
        paddingBottom: `${mapP(10, 40, progress)}pt`,
    }
    return <div className={styles.header}>
        <h3 style={{
            ...animation,
        }}>Пример использования</h3>
    </div>
}

export const ChatBlock = () => {
    const {chatBlock: {ref}} = useHomeParallaxContext();
    const date = new Date().toLocaleDateString('ru', {day: 'numeric', month: 'long'})
    return <div ref={ref}>
        <div className={styles.container}>
            <HeaderChatBlock/>
            <YandexChat date={date} messages={
                getConversation(conversations)
            }/>
        </div>
    </div>
};
