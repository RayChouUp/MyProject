import { post } from "../request";


export const createRemind = (payload) => post('/remind', payload)