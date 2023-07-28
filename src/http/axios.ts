import axios, { AxiosRequestConfig, AxiosResponse, AxiosPromise } from 'axios'
import { showMessage } from './status'
import { ElMessage } from 'element-plus'

const defaultConfig = {
    timeout: 1000,
    baseURL: import.meta.env.VITE_APP_URL
}
export const axiosInstance = axios.create(defaultConfig)

//http request 拦截器
axiosInstance.interceptors.request.use(
    (config: AxiosRequestConfig) => {
        // 配置请求头
        config.headers = {
            //'Content-Type':'application/x-www-form-urlencoded',
            'Content-Type': 'application/json;charset=UTF-8',
            // 'token': '80c483d59ca86ad0393cf8a98416e2a1'
            Authorization: localStorage.getItem('jwt-token') || ''
        }
        return config
    },
    (error: any) => {
        return Promise.reject(error)
    }
)

//http response 拦截器
axiosInstance.interceptors.response.use(
    (response: AxiosResponse) => {
        return response
    },
    (error) => {
        const { response } = error
        if (response) {
            // 请求已发出，但是不在2xx的范围
            showMessage(response.status)
            return Promise.reject(response.data)
        } else {
            ElMessage.warning('网络连接异常,请稍后再试!')
        }
    }
)

// 封装 GET POST 请求并导出
export function request(url = '', params = {}, type = 'POST') {
    //设置 url params type 的默认值
    return new Promise<any>((resolve, reject) => {
        let promise
        if (type.toUpperCase() === 'GET') {
            promise = axiosInstance({
                url,
                params
            })
        } else if (type.toUpperCase() === 'POST') {
            promise = axiosInstance({
                method: 'POST',
                url,
                data: params
            })
        } else if (type.toUpperCase() === 'DELETE') {
            promise = axiosInstance({
                method: 'DELETE',
                url,
                data: params
            })
        }
        //处理返回
        ;(promise as AxiosPromise)
            .then((res) => {
                resolve(res)
            })
            .catch((err) => {
                reject(err)
            })
    })
}
