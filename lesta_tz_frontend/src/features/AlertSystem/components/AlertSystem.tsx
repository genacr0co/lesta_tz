import {Props} from "../lib/props";
import {useAlerts} from "@/features/AlertSystem/lib/useAlerts";

export const AlertSystem = (props: Props) => {
    const {contextHolder} = useAlerts();
    return contextHolder;
};