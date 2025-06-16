import axios from 'axios';
import Cookies from "js-cookie";
import getConfig from "next/config";
import {createTrigger} from "trigger-man";
import Router from 'next/router';
import {Cookies as ReactCookies} from "react-cookie";

import {isTokenExpired} from "@/shared/lib/helpers";
import {postRefreshTokens} from "@/shared/api/services";

const {publicRuntimeConfig} = getConfig();

export const $main_instances = axios.create({
    baseURL: publicRuntimeConfig.NEXT_PUBLIC_DOMAIN,
});

$main_instances.interceptors.request.use(async (config) => {

    if (!config?.headers) {
        throw new Error('Expected \'config\' and \'config.headers\' not to be undefined');
    }

    if (!Cookies.get('access') || isTokenExpired(Cookies.get('access'))) {
        await postRefreshTokens().then((r) => {
            if (r.status === 200) {
                Cookies.set('access', r.data.access_token)
                Cookies.set('refresh', r.data.refresh_token)
            } else {
                window.location.href = '/login'
            }
            config.headers.Authorization = `Bearer ${r.data.access_token}`;

        }).catch(e => {
            createTrigger('alert', {message: 'Refresh Token Expired', type: 'error'})

            Cookies.remove('access')
            Cookies.remove('refresh')
            const cookies = new ReactCookies();
            cookies.remove('access')
            cookies.remove('refresh')

            Router.replace('/login');
        })
    } else {
        config.headers.Authorization = `Bearer ${Cookies.get('access')}`;
    }

    return config;
});
