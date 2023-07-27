import { request } from '@/http/axios'

export const getAllExps = (url: string) => {
    return request(url, {}, 'GET')
}

export const updateExpName = (url: string, params: any) => {
    return request(url, params, 'POST')
}

export const getExpsList = (url: string, params: any) => {
    return request(url, params, 'GET')
}

export const getExpDetail = (url: string, params: any) => {
    return request(url, params, 'GET')
}
