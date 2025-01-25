import {ReactNode} from "react";
import {css} from "@emotion/css";

interface Content {
    text: ReactNode
    url?: string
}

function ContentBlock({text, url}: Content) {
    const children = url ? <a target="_blank" href={url}>
        {text}
    </a> : text
    return <li>
        {children}
    </li>
}


interface Props {
    contents?: Content[];
}

export function FooterContent({contents}: Props) {
    return <ul className={css`list-style: none;
        padding: 0;
        margin: 0;`}>
        {contents?.map((content, index) => (
            <ContentBlock {...content} key={index}/>
        ))}
    </ul>
}
