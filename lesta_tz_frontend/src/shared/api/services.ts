import axios, {AxiosResponse} from 'axios';
import Cookies from "js-cookie";
import getConfig from "next/config";


import {urls} from './urls';
import * as types from './types';


const {publicRuntimeConfig} = getConfig();

const $axios = axios.create({
    withCredentials: true,
    baseURL: publicRuntimeConfig.NEXT_PUBLIC_DOMAIN,
});

$axios.interceptors.request.use(async (config) => {
    if (!config?.headers) {
        throw new Error('Expected \'config\' and \'config.headers\' not to be undefined');
    }
    config.headers.Authorization = `Bearer ${Cookies.get('refresh')}`;
    return config
});

export async function postRefreshTokens(): Promise<AxiosResponse<types.IPostRefreshTokensResponse>> {
    return await $axios.post<types.IPostRefreshTokensResponse>(urls.postRefreshTokens());
}
