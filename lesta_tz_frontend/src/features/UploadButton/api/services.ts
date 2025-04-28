import {AxiosResponse} from 'axios';

import {urls} from './urls';
import * as types from './types';
import {$instances} from "./instances";

export async function postUploadFile(params: types.IPostUploadFileParams): Promise<AxiosResponse<types.IPostUploadFileResponse>> {
    const formData = new FormData();
    formData.append('file', params.file);

    return await $instances.post<types.IPostUploadFileResponse>(urls.postUploadFile(), formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}