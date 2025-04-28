import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function getDocumentContent(params: types.IGetDocumentContentParams): Promise<AxiosResponse<types.IGetDocumentContent>> {
    return await $instances.get<types.IGetDocumentContent>(urls.getDocumentContent(params.document_id), {
        params
    });
}