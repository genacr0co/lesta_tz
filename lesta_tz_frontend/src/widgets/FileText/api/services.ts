import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$main_instances} from "@/shared/api/instances";

export async function getDocumentContent(params: types.IGetDocumentContentParams): Promise<AxiosResponse<types.IGetDocumentContent>> {
    return await $main_instances.get<types.IGetDocumentContent>(urls.getDocumentContent(params.document_id), {
        params
    });
}