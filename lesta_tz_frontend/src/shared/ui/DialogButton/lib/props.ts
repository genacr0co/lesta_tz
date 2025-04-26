import {ReactNode, MouseEventHandler} from "react";

export interface Props {
    title?: string;
    children?: ReactNode;
    onClick?: MouseEventHandler<HTMLDivElement>;
}