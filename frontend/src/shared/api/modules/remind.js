import { post,get } from "../request";


export const createRemind = (payload) => post('/remind', payload)

export const getReminds = (limit) => get('/remind', { limit })