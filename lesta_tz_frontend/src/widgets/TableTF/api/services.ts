import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function getWordList(params: types.IGetWordListParams): Promise<AxiosResponse<types.IGetWordList>> {
    return await $instances.get<types.IGetWordList>(urls.getWordList(params.document_id), {
        params
    });
}