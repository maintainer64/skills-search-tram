import {css} from "@emotion/css";
import {ReactNode} from "react";
import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {mapP} from "@/components/parallax-providers/map-scroll-effect";


interface Props {
    title: string;
    subtitle: string;
    image: string;
    background: string;
    hoverText: string;
    icon: ReactNode;
}

const styles = {
    title: css`
        position: absolute;
        bottom: 8px;
        right: 10px;
        font-size: 18pt;
        font-weight: bold;
    `,
    subtitle: css`
        position: absolute;
        top: 8px;
        left: 10px;
        font-size: 24pt;
    `,
    card: css`
        position: relative;
        height: 80vh;
        width: 30vw;
        overflow: hidden;
        @media (max-width: 768px) {
            height: 40vh;
            width: auto;
        }
        color: white !important;
    `,
    background: css`
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    `,
    svg: css`
        position: absolute;
        top: 8px;
        right: 10px;
        font-size: 24pt;
        width: 20%;
        height: 20%;
    `,
    hoverBlock: css`
        & {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
            filter: brightness(100%) blur(0px);
        }

        & + .hover-text {
            opacity: 0;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24pt;
            font-weight: bold;
            color: white;
        }

        &:hover {
            filter: brightness(80%) blur(5px);
        }

        &:hover + .hover-text {
            opacity: 1;
        }
    `,
}

const AccessibilityCard = ({
                               title,
                               subtitle,
                               background,
                               image,
                               icon,
                               hoverText,
                           }: Props) => {
    const {availableBlock: {progress}} = useHomeParallaxContext();
    const animation = {
        coverBackgroundPosition: mapP(-25, 100, progress),
    }
    return (
        <div className={styles.card}>
            <div className={styles.hoverBlock}>
                <div style={{
                    background: `center / cover no-repeat url("/${background}")`,
                    opacity: 0.4
                }} className={styles.background}></div>
                <div className={styles.svg}>{icon}</div>
                <div style={{
                    background: `center / cover no-repeat url("/${image}")`,
                    backgroundPositionY: `${animation.coverBackgroundPosition}%`
                }} className={styles.background}></div>
                <div className={styles.title}>{title}</div>
                <div className={styles.subtitle}>{subtitle}</div>
            </div>
            <div className="hover-text">{hoverText}</div>
        </div>
    );
};

export default AccessibilityCard;
