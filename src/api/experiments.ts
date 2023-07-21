import { request } from '@/http/axios'

export const getAllExps = (url: string) => {
    return request(url, {}, 'GET')
}
