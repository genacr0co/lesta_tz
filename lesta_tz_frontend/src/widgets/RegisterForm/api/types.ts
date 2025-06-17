
export interface IRegisterRequestBody {
    name: string;
    email: string;
    password: string;
}

export interface IRegisterResponseBody {
    id: number;
    email: string;
    name: string;
}