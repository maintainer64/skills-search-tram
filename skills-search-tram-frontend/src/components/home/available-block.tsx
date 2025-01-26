'use client'


import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {css} from "@emotion/css";
import AccessibilityBlock from "@/components/assistants";
import {mapP, rangeP} from "@/components/parallax-providers/map-scroll-effect";

const styles = {
    container: css`
        display: block;
        position: relative;
        height: inherit;
    `,
    header: css`
        & {
            padding: 20pt 0;
        }

        & > h3 {
            color: white !important;
        }

    `,
}

export function HeaderAvailableBlock() {
    const {availableBlock: {progress}} = useHomeParallaxContext();
    const animation = {
        opacity: rangeP(
            0,
            0.4,
            progress
        ),
        paddingTop: `${mapP(20, 200, progress)}pt`,
        paddingBottom: `${mapP(10, 40, progress)}pt`,
    }
    return <div className={styles.header}>
        <h3 style={{
            ...animation,
        }}>Используйте на устройствах</h3>
    </div>
}

export const AvailableBlock = () => {
    const {availableBlock: {ref}} = useHomeParallaxContext();
    return <div style={{height: 'inherit'}} ref={ref}>
        <HeaderAvailableBlock/>
        <div className={styles.container}>
            <AccessibilityBlock/>
        </div>
    </div>
};
