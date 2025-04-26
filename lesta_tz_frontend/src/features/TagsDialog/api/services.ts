import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function getTagList(): Promise<AxiosResponse<types.ITagsResponse>> {
    return await $instances.get<types.ITagsResponse>(urls.getTagList());
}