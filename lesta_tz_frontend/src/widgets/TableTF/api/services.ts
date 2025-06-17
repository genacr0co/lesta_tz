import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$main_instances} from "@/shared/api/instances";

export async function getWordList(params: types.IGetWordListParams): Promise<AxiosResponse<types.IGetWordList>> {
    return await $main_instances.get<types.IGetWordList>(urls.getWordList(params.document_id), {
        params
    });
}