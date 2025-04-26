import {ReactNode, MouseEventHandler} from "react";

export interface Props {
    children?: ReactNode;
    disabled?: Boolean;
    onClick?: MouseEventHandler<HTMLDivElement>;
    fixed?: Boolean;
    selected?: Boolean;
}