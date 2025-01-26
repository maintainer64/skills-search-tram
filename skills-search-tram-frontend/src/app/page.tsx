'use client'
import {HomeComponent} from "@/components/home";
import {ParallaxHomeProvider} from "@/components/parallax-providers/home/provider";

export default function Home() {
    return (
        <ParallaxHomeProvider>
            <HomeComponent/>
        </ParallaxHomeProvider>
    );
}
