import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function postlogin(data: types.ILoginRequestBody): Promise<AxiosResponse<types.ILoginResponseBody>> {
    return await $instances.post<types.ILoginResponseBody>(urls.postlogin(), data);
}

