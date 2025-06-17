import React from "react";
import Head from "next/head";
import {withLoginRoute} from "@/processes";
import {RegisterForm} from "@/widgets"

const Register = () => {
    return (
        <>
            <Head>
                <title>Register</title>
                <meta name="description" content="Register page"/>
            </Head>
            <RegisterForm/>
        </>
    );
}

export default withLoginRoute(Register);

