import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function getDocsList(): Promise<AxiosResponse<types.IDocList>> {
    return await $instances.get<types.IDocList>(urls.getDocsList());
}

export async function deleteDocument(params: types.IDeleteDocumentParams): Promise<AxiosResponse<types.IDeleteDocumentResponse>> {
    return await $instances.delete<types.IDocList>(urls.deleteDocument(params.document_id), {
        params
    });
}

