import {ReactNode, MouseEventHandler} from "react";

export interface Props {
    children?: ReactNode;
    disabled?: Boolean;
    onClickTitle?: MouseEventHandler<HTMLDivElement>;
    fixed?: Boolean;
    selected?: Boolean;
    title?: String;
}