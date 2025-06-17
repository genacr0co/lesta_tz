import React from "react";
import Head from "next/head";
import {withLoginRoute} from "@/processes";
import {LoginForm} from "@/widgets"

const Login = () => {
    return (
        <>
            <Head>
                <title>Login</title>
                <meta name="description" content="Login page"/>
            </Head>
            <LoginForm/>
        </>
    );
}

export default withLoginRoute(Login);

