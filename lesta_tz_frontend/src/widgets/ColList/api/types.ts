
export interface IGetColRequestBody {
    page: number;
    page_size: number;
}

export interface ICol {
    id: number;
    name: string;
}

export interface IGetColResponseBody {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
    results: ICol[];
}