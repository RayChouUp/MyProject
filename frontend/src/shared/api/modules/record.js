import { post,get } from "../request";

export const createRecord = (payload) => post('/record', payload)

export const getRecords = (limit) => get('/record', { limit })