import {ReactNode} from "react";
import {css} from "@emotion/css";

interface Props {
    children?: ReactNode;
}

export function FooterContainer({children}: Props) {
    return <footer className={css`
        display: flex;
        justify-content: space-around;
        line-height: 20pt;
        font-weight: 400;

        & a {
            color: inherit;
            cursor: pointer;
            opacity: 98%;
            text-decoration: none;
            transition: all 0.3s linear;
        }

        & a:hover {
            opacity: 50%;
        }
    `}>
        {children}
    </footer>
}
