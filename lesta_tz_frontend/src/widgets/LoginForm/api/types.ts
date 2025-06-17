
export interface ILoginRequestBody {
    password: string;
    email: string;
}

export interface ILoginResponseBody {
    access_token: string;
    refresh_token: string;
}