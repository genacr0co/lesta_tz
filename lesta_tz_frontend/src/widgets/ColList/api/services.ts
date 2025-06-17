import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$main_instances} from "@/shared/api/instances";

export async function getColList(params:types.IGetColRequestBody): Promise<AxiosResponse<types.IGetColResponseBody>> {
    return await $main_instances.get<types.IGetColResponseBody>(urls.getColList(), {params});
}



