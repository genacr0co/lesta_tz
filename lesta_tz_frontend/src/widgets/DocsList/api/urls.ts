export const urls = {
    getDocsList() {
        return `/api/documents`;
    },
    deleteDocument(document_id: number) {
        return `/api/document/${document_id}`;
    },
 
};