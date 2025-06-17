import {notification} from "antd";
import {ArgsProps, IconType} from "antd/es/notification/interface";
import {useTrigger} from "trigger-man";
import { TRIGGER } from "@/shared/const";

export const useAlerts = () => {
    const [api, contextHolder] = notification.useNotification();
    const openNotification = (message: string, type?: IconType) => {

        const data: ArgsProps = {
            message,
            placement: "topRight",
            duration: 3
        }

        switch (type) {
            case 'info':
                api.info(data);
                break;
            case 'success':
                api.success(data);
                break;
            case 'warning':
                api.warning(data);
                break;
            default:
                api.error(data);
        }
    };

    useTrigger(TRIGGER.ALERT, (event) => {
        openNotification(event.detail.message, event.detail.type);
    })

    return {
        contextHolder, api, openNotification
    }
}