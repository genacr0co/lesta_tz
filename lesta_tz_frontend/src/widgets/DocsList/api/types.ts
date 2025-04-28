
export interface IDocItem {
    id: number;
    filename: string;
}

export interface IDocList {
    results: IDocItem[];
}

export interface IDeleteDocumentParams {
    document_id: number;
}

export interface IDeleteDocumentResponse {

}
