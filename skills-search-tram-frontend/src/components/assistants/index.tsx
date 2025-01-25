import {css} from "@emotion/css";
import {IconYandex} from "@/components/assistants/icon-yandex";
import {IconVK} from "@/components/assistants/icon-vk";
import {IconSber} from "@/components/assistants/icon-sber";
import AccessibilityCard from "@/components/assistants/card";

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
    const items = [
        {
            title: 'Алиса',
            subtitle: 'Станция',
            image: 'assistant_alice.png',
            icon: <IconYandex/>,
        },
        {
            title: 'Салют',
            subtitle: 'Boom',
            image: 'assistant_salute.png',
            icon: <IconSber/>,
        },
        {
            title: 'Маруся',
            subtitle: 'Капсула',
            image: 'assistant_marusya.png',
            icon: <IconVK/>,
        },
    ];

    return (
        <div className={styles.container}>
            {items.map((item, index) => (
                <div className={styles.card} key={index}>
                    <AccessibilityCard {...item}/>
                </div>
            ))}
        </div>
    );
};

export default AccessibilityBlock;
