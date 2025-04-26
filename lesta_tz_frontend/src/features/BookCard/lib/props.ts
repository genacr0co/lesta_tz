import {ReactNode, MouseEventHandler} from "react";

export interface Props {
    onClick?: MouseEventHandler<HTMLDivElement>;
    id: number;
    title: string;
    price: number;
    date: string;
    author: string;
    tags: string[];
}


