import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function postRegister(data: types.IRegisterRequestBody): Promise<AxiosResponse<types.IRegisterResponseBody>> {
    return await $instances.post<types.IRegisterResponseBody>(urls.postRegister(), data);
}

