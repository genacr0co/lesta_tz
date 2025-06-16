import {createTrigger} from "trigger-man";
import {undefined} from "zod";

export function parseJwt(token: string) {
    let base64Url = token.split('.')[1];

    if (base64Url) {
        let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        let jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    }

    return undefined;
}

export function isTokenExpired(token: string | undefined) {
    if (!token) {
        console.log(token)
        return true
    }
    if (parseJwt(token) === undefined) {
        console.log(parseJwt(token))
        return true
    }
    const decoded = parseJwt(token);
    return Date.now() >= decoded.exp * 1000;
}

export const catchErrors = (e: any) => {
    if (e.response) {
        if (e.response.status == 422){
            const msg = e.response.data.detail[0].msg
            const loc = e.response.data.detail[0].loc[1]
            createTrigger('alert', {message: `${msg} : ${loc}`, type: 'error'})
        }
        else if (e.response.status < 500) {
            try {
                createTrigger('alert', {message:  e.response.data.detail, type: 'error'})
            }
            catch (e) {
                createTrigger('alert', {message: "Undefined Error", type: 'error'})
            }
            
        } else {
            createTrigger('alert', {message: `${e.response.status} server error`, type: 'error'})
        }
    }
}
