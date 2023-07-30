import { request } from '@/http/axios'

export const getAllExps = (url: string) => {
    return request(url, {}, 'GET')
}

// put
export const updateExpName = (url: string, params: any) => {
    return request(url, params, 'POST')
}

// delete
export const deleteExpName = (url: string, params: any) => {
    return request(url, params, 'DELETE')
}

export const getExpsList = (url: string, params: any) => {
    return request(url, params, 'GET')
}

export const getExpDataset = (url: string) => {
    return request(url, {}, 'GET')
}

export const updateExpDetail = (url: string, params: any) => {
    return request(url, params, 'POST')
}

export const deleteExpDetail = (url: string, params: any) => {
    return request(url, params, 'DELETE')
}

export const getExpDetail = (url: string, params: any) => {
    return request(url, params, 'GET')
}

export const getExpStatistic = (url: string, params: any) => {
    return request(url, params, 'GET')
}

export const getPerExpStatistic = (url: string, params: any) => {
    return request(url, params, 'GET')
}
