'use client'

import {css} from "@emotion/css";
import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {mapP} from "@/components/parallax-providers/map-scroll-effect";
import {metaInfo} from "@/components/meta";

export const HelloMainComponent = () => {
    const {helloSecondBlock: {ref, progress}} = useHomeParallaxContext()
    const titleProgress = {
        opacity: progress * 2,
        lintHeight: mapP(30, 100, progress)
    }
    const descriptionProgress = {
        opacity: progress * 2,
        lintHeight: mapP(10, 46, progress)
    }
    return <main ref={ref}>
        <h1 style={{
            opacity: titleProgress.opacity,
            lineHeight: `${titleProgress.lintHeight}pt`,
        }} className={css`
            font-size: 80pt;
            margin: 80pt 0;
            position: relative;
            font-weight: 800;
            top: 150px;
            left: 10%;
            width: fit-content;
        `}>
            {metaInfo.titleHtml}
        </h1>
        <p
            style={{
                opacity: descriptionProgress.opacity,
                lineHeight: `${descriptionProgress.lintHeight}pt`,
            }}
            className={css`
                font-size: 38pt;
                color: var(--foreground);
                position: relative;
                top: 120px;
                left: 10%;
                width: fit-content;
                max-width: 70%;
            `}>
            {metaInfo.description}
        </p>
    </main>
};
