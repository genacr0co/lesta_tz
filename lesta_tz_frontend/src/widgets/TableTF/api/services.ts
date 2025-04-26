import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";
import {IBookItem} from "./types";

export async function getBookList(params?: types.IGetBookListParams): Promise<AxiosResponse<types.IBookItem[]>> {
    return await $instances.get<types.IBookItem[]>(urls.getBookList(), {
        params
    });
}