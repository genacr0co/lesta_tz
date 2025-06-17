export const urls = {
    getWordList(document_id: number) {
        return `/api/v1/document/${document_id}/statistics`;
    },
};