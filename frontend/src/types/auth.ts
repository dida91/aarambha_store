export type UserRole = 'CUSTOMER' | 'SELLER' | 'ADMIN'

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: UserRole
  phone: string
}

export interface RegisterPayload {
  username: string
  email: string
  password: string
  first_name: string
  last_name: string
  phone: string
}

export interface LoginPayload {
  username: string
  password: string
}

export interface TokenPair {
  access: string
  refresh: string
}
