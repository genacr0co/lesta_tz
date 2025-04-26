
export type TFilterName = undefined | '' | 'price' | 'author' | 'date';

export interface IFilterBy {
    name: TFilterName;
    order: boolean; // true is 'desc'
}

export interface IBookItem {
    id: number;
    title: string;
    author: string;
    date: string;
    price: number;
    tags: string[];
}

export interface IGetBookListParams {
    tags?: string[];
    sendAll?: boolean;
    filterBy?: IFilterBy;
}

