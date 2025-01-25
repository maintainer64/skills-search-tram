'use client'

import {createContext, Dispatch, RefObject, useContext} from 'react';

interface IParallaxRef<T> {
    ref?: RefObject<T>;
    progress: number;
    setProgress: Dispatch<number>
}

interface IParallaxContext {
    helloSecondBlock: IParallaxRef<HTMLHeadingElement>
    chatBlock: IParallaxRef<HTMLHeadingElement>
    availableBlock: IParallaxRef<HTMLHeadingElement>
}

export const ParallaxHomeContext = createContext<IParallaxContext>({
    helloSecondBlock: {
        ref: undefined,
        progress: 0,
        setProgress: () => {
        }
    },
    chatBlock: {
        ref: undefined,
        progress: 0,
        setProgress: () => {
        }
    },
    availableBlock: {
        ref: undefined,
        progress: 0,
        setProgress: () => {
        }
    },
});
export const useHomeParallaxContext = () => useContext(ParallaxHomeContext);
