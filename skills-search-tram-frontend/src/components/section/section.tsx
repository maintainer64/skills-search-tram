'use client'

import {ReactNode} from "react";
import {css} from "@emotion/css";


interface Props {
    fixed?: boolean;
    children?: ReactNode;
    minHeight?: string;
    className?: string;
    background?: string;
}

export function SectionComponent({fixed, children, className, minHeight, background}: Props) {
    const position = fixed ? 'sticky' : 'relative';
    const styles = {
        section: css`
            & {
                top: 0;
                position: ${position};
                display: block;
                min-height: ${minHeight ?? '100vh'};
                background: ${background ?? 'inherit'};
            }

            & h3 {
                font-size: 40pt;
                text-align: left;
                margin-left: 10pt;
                color: var(--foreground);
            }
        `
    }
    return <section className={css(styles.section, className)}>{children}</section>
}
