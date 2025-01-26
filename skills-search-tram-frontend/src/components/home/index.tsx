'use client'
import {SectionComponent} from "@/components/section/section";
import {HelloMainComponent} from "@/components/home/hello-block";
import {AnimationRive} from "@/components/home/animation-block";
import {FooterComponent} from "@/components/footer/footer";
import {ChatBlock} from "@/components/home/chat-block";
import {AvailableBlock} from "@/components/home/available-block";


export const HomeComponent = () => {
    return <div>
        {/* Первый блок */}
        <SectionComponent fixed={true}>
            <AnimationRive/>
        </SectionComponent>
        <SectionComponent>
            <HelloMainComponent/>
        </SectionComponent>
        <SectionComponent background={'#fff'}>
            <ChatBlock/>
        </SectionComponent>
        <SectionComponent background={'#000'}>
            <AvailableBlock/>
        </SectionComponent>
        {/* Последний блок */}
        <SectionComponent background={'#fff'}>
            <FooterComponent/>
        </SectionComponent>
    </div>
};
