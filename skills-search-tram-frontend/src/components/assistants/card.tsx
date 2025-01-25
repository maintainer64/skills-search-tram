import {css} from "@emotion/css";
import {ReactNode} from "react";
import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {mapP} from "@/components/parallax-providers/map-scroll-effect";


interface Props {
    title: string;
    subtitle: string;
    image: string;
    icon: ReactNode;
}

const styles = {
    title: css`
        position: absolute;
        bottom: 8px;
        right: 10px;
        font-size: 18pt;
        font-weight: bold;
        color: white;
    `,
    subtitle: css`
        position: absolute;
        top: 8px;
        left: 10px;
        font-size: 24pt;
        color: white;
    `,
    card: css`
        position: relative;
        height: 80vh;
        width: 30vw;
        @media (max-width: 768px) {
            height: 40vh;
            width: auto;
        }
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
}

const AccessibilityCard = ({
                               title,
                               subtitle,
                               image,
                               icon,
                           }: Props) => {
    const {availableBlock: {progress}} = useHomeParallaxContext();
    const animation = {
        coverBackgroundPosition: mapP(-25, 100, progress)
    }
    return (
        <div className={styles.card}>
            <div className={styles.svg}>{icon}</div>
            <div style={{
                background: `center / cover no-repeat url("/${image}")`,
                backgroundPositionY: `${animation.coverBackgroundPosition}%`
            }} className={styles.background}></div>
            <div className={styles.title}>{title}</div>
            <div className={styles.subtitle}>{subtitle}</div>
        </div>
    );
};

export default AccessibilityCard;
