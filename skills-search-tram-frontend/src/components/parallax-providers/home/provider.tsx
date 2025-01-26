'use client'

import {ReactNode} from "react";
import {useParallaxRef} from "@/components/parallax-providers/use-parallax-ref";
import {ParallaxHomeContext} from "@/components/parallax-providers/home/context";

interface Props {
    children?: ReactNode;
}

export function ParallaxHomeProvider({children}: Props) {
    const helloSecondBlock = useParallaxRef<HTMLHeadingElement>();
    const chatBlock = useParallaxRef<HTMLHeadingElement>();
    const availableBlock = useParallaxRef<HTMLHeadingElement>();
    return <ParallaxHomeContext.Provider value={{helloSecondBlock, chatBlock, availableBlock}}>
        {children}
    </ParallaxHomeContext.Provider>
}
