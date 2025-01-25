'use client'
import {ChatMessageProps} from "@/components/chat/types";


export const metaInfo = {
    titleHtml: <>Когда <br/> приедет</>,
    description: "Навык расписания ближайшего общественного транспорта для умных устройств и ассистентов",
    copyright: {
        name: 'Д. Д. Губанов',
        url: 'https://gubanov.site',
        year: 2025
    },
};

export const conversations: ChatMessageProps[][] = [
    [
        {
            text: 'запусти навык когда приедет',
            bot: false,
        },
        {
            text: 'Запускаю навык «Когда приедет»',
            bot: true,
        },
        {
            text: 'Скажите номер автобуса, трамвая или троллейбуса, и я подскажу, когда он прибудет на ближайшую остановку.',
            bot: true,
        },
        {
            text: '18 трамвай',
            bot: false,
        },
        {
            text: 'До станции Шарташ прибудет через 2 минуты. Затем через 22 минуты.\n' +
                'До станции Волгоградская прибудет через 19 минут. Затем в 10 часов 33 минуты.',
            bot: true,
        }
    ]
]

export function getConversation(conversations: ChatMessageProps[][]) {
    const random = Math.floor(Math.random() * conversations.length);
    return conversations[random]
}
