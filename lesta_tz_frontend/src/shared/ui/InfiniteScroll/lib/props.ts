import {Dispatch, ReactNode, SetStateAction} from "react";

export interface Props {
    children?: ReactNode;

    page: number;
    pageSize: number;
    count: number;
    loading: boolean;

    setPage: (page: number) => void | Dispatch<SetStateAction<number>>;
    root?: string;
    lastElementCurrent?: HTMLElement | null;
    debug?: boolean;
    listLength: number;
}