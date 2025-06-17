export interface IGetDocumentContent {
    id: number;
    filename: string;
    content: string;
}

export interface IGetDocumentContentParams {
    document_id: number;
}