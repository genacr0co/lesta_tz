
export interface IGetWordList {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
    results: IGetWordListItem [];
}

export interface IGetWordListItem {
    word: string;
    tf: number;
    idf: number;
}

export interface IGetWordListParams {
    document_id: number;
    page?: number;
    page_size?: number;
    collection_id: number;
}

