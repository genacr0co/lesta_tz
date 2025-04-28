import axios from 'axios';

export const $instances = axios.create({
    baseURL: process.env.NEXT_PUBLIC_DOMAIN,
});

$instances.interceptors.request.use(async (config) => {

    if (!config?.headers) {
        throw new Error('Expected \'config\' and \'config.headers\' not to be undefined');
    }

    return config;
});
