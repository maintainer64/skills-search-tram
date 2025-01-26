import {ReactNode} from "react";
import {css} from "@emotion/css";

interface Props {
    children?: ReactNode;
}

export function FooterHeadline({children}: Props) {
    return <h5 className={css`font-weight: bold;`}>{children}</h5>
}
