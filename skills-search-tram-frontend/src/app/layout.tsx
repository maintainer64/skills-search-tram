import type {Metadata} from "next";
import "./reset.css";
import "./globals.css";
import {Providers} from './providers';
import {ReactNode} from "react";
import {Montserrat} from 'next/font/google'


const montserrat = Montserrat({
    weight: ['200', '400', '700'],
    style: ['normal', 'italic'],
    subsets: ['latin'],
    display: 'swap',
})


export const metadata: Metadata = {
    title: "Когда приедет",
    description: "Навык расписания ближайшего общественного транспорта для умных устройств и ассистентов",
    icons: {icon: "/favicon.png", apple: "/favicon.png"},
    authors: {
        name: 'Danil Gubanov',
        url: 'https://gubanov.site',
    },
};

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: ReactNode;
}>) {
    return (
        <html lang="ru" suppressHydrationWarning={true}>
        <body
            suppressHydrationWarning={true}
            className={montserrat.className}
        >
        <Providers>{children}</Providers>
        </body>
        </html>
    );
}
