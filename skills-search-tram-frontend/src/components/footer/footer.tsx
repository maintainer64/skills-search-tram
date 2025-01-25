'use client'

import {metaInfo} from "@/components/meta";
import {FooterContent} from "@/components/footer/content";
import {FooterContainer} from "@/components/footer/container";
import {FooterHeadline} from "@/components/footer/headline";

export const FooterComponent = () => {
    return <FooterContainer>
        <div>
            <FooterHeadline>
                О сайте
            </FooterHeadline>
            <FooterContent contents={[
                {
                    text: (<>© <a href={metaInfo.copyright.url} target="_blank">
                        {metaInfo.copyright.name}
                    </a>, {metaInfo.copyright.year}</>)
                },
                {
                    text: 'Карта сайта',
                    url: '/sitemap.xml'
                },
                {
                    text: (
                        <>Размещенные данные носят<br/>информационный характер и не<br/>являются публичной
                            офертой</>
                    )
                },
            ]}/>
        </div>
        <div>
            <FooterHeadline>
                Ссылки
            </FooterHeadline>
            <FooterContent contents={[
                {
                    text: 'Github...',
                },
                {
                    text: 'VK...',
                },
                {
                    text: 'Telegram...',
                },
                {
                    text: 'Whatsapp...',
                },
            ]}/>
        </div>
        <div>
            <FooterHeadline>
                Навыки
            </FooterHeadline>
            <FooterContent contents={[
                {
                    text: 'Yandex',
                },
                {
                    text: 'Sber',
                },
                {
                    text: 'Vk',
                },
            ]}/>
        </div>
    </FooterContainer>
};
