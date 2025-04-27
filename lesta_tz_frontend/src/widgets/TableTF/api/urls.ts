export const urls = {
    getWordList(document_id: number) {
        return `/api/document/${document_id}/words`;
    },
};