import NextNProgress from "nextjs-progressbar";

import {Props} from "../lib/props";

export const ProgressLoader = (props: Props) => {

    return (
        <NextNProgress color={"#397af5"} options={{showSpinner: false}}/>
    );
};