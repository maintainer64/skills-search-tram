'use client'
import {Alignment, Fit, Layout, useRive} from "@rive-app/react-canvas";
import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {css} from "@emotion/css";
import {mapP} from "@/components/parallax-providers/map-scroll-effect";

export const AnimationRive = () => {
    const {helloSecondBlock: {progress}} = useHomeParallaxContext();

    const {RiveComponent, rive} = useRive({
        src: "/when_arrive.riv",
        animations: ['Translate', 'Intro', 'NoIntro'],
        stateMachines: ['Way'],
        layout: new Layout({
            fit: Fit.FitWidth,
            alignment: Alignment.Center,
        }),
        onLoad: () => {
            rive?.resizeDrawingSurfaceToCanvas();
        },
        autoplay: true,
    });

    return <div className={css`
        position: absolute;
        height: 100vh;
        background: #cf9ca5;
        width: 100%;
        margin: 0 0 100vh 0;
        padding: 0;
    `} style={{opacity: mapP(1, 0.31, progress)}}>
        <RiveComponent height="1920" width="1080"/>
    </div>;
};
