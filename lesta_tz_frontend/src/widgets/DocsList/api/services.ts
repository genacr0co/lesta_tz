import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function getDocsList(): Promise<AxiosResponse<types.IDocList>> {
    return await $instances.get<types.IDocList>(urls.getDocsList());
}