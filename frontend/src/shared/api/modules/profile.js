import { get, put } from '../request'

export const fetchProfile = () => get('/profile')

export const updateProfile = (payload) => put('/profile', payload)
