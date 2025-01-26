import {css} from "@emotion/css";
import {IconYandex} from "@/components/assistants/icon-yandex";
import {IconVK} from "@/components/assistants/icon-vk";
import {IconSber} from "@/components/assistants/icon-sber";
import AccessibilityCard from "@/components/assistants/card";
import {useHomeParallaxContext} from "@/components/parallax-providers/home/context";
import {mapP} from "@/components/parallax-providers/map-scroll-effect";

const styles = {
    container: css`
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 16px;
        padding: 16px;
        background-color: black;
        height: 100%;

        @media (max-width: 768px) {
            flex-direction: column;
            align-items: center;
        }
    `,
    card: css`
        background-color: black;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        text-align: center;

        @media (max-width: 768px) {
            width: 90%;
        }
    `,
}

const AccessibilityBlock = () => {
    const {availableBlock: {progress}} = useHomeParallaxContext();
    const items = [
        {
            title: 'Алиса',
            subtitle: 'Станция',
            hoverText: 'На модерации',
            image: 'assistant_alice.png',
            background: 'assistant_alice_bg.png',
            icon: <IconYandex/>,
        },
        {
            title: 'Салют',
            subtitle: 'Boom',
            hoverText: 'В разработке',
            image: 'assistant_salute.png',
            background: 'assistant_salute_bg.png',
            icon: <IconSber/>,
        },
        {
            title: 'Маруся',
            subtitle: 'Капсула',
            hoverText: 'В разработке',
            image: 'assistant_marusya.png',
            background: 'assistant_marusya_bg.png',
            icon: <IconVK/>,
        },
    ];
    const scale = mapP(0.95, 1, progress);

    return (
        <div className={styles.container}>
            {items.map((item, index) => (
                <div style={{
                    transform: `scale(${scale})`
                }} className={styles.card} key={index}>
                    <AccessibilityCard {...item}/>
                </div>
            ))}
        </div>
    );
};

export default AccessibilityBlock;
