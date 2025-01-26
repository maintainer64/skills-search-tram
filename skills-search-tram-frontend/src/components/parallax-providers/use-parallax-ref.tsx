'use client'

import {useParallax} from "react-scroll-parallax";
import {useState} from "react";
import {useDebounce} from "use-debounce";


export function useParallaxRef<T extends HTMLElement>() {
    const [progressValue, setProgress] = useState<number>(0);
    const [progress] = useDebounce(progressValue, 5);
    const parallax = useParallax<T>({
        onProgressChange: (progress) => {
            if (parallax.ref.current) {
                // set progress to CSS variable
                setProgress(progress)
            }
        },
    });
    return {ref: parallax.ref, progress, setProgress};
}
