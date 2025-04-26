import {ReactNode, MouseEventHandler} from "react";

export interface Props {
    children?: ReactNode;
    onClick?: MouseEventHandler<HTMLDivElement>;
}