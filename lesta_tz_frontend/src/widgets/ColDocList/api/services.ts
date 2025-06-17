import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$main_instances} from "@/shared/api/instances";

export async function getColDocsList(params: types.IGetColDocumentParams): Promise<AxiosResponse<types.IGetColDocumentResponse>> {
    return await $main_instances.get<types.IGetColDocumentResponse>(urls.getColDocsList(params.collection_id), {params});
}

