'use client'

import {ReactNode} from "react";

export interface ChatMessageProps {
    text: ReactNode,
    bot: boolean
}

export interface ChatProps {
    messages: ChatMessageProps[],
    date: string
}
