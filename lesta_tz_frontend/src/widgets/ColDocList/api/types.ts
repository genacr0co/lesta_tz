
export interface IColDoc {
    id: number;
    filename: string;
    file_path: string;
    owner_id: number;
}

export interface IGetColDocumentParams {
    collection_id: number;
    page: number;
    page_size: number;
}

export interface IGetColDocumentResponse {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
    documents: IColDoc[];
}