import { apiClient, unwrapEnvelope } from '../../lib/api'
import { API_ENDPOINTS } from '../../lib/endpoints'
import type { ApiEnvelope } from '../../types/api'
import type { LoginPayload, RegisterPayload, TokenPair, User } from '../../types/auth'

export async function login(payload: LoginPayload): Promise<TokenPair> {
  const response = await apiClient.post<ApiEnvelope<TokenPair>>(API_ENDPOINTS.accounts.login, payload)
  return unwrapEnvelope(response.data)
}

export async function register(payload: RegisterPayload): Promise<User> {
  const response = await apiClient.post<ApiEnvelope<User>>(API_ENDPOINTS.accounts.register, payload)
  return unwrapEnvelope(response.data)
}

export async function fetchCurrentUser(): Promise<User> {
  const response = await apiClient.get<ApiEnvelope<User>>(API_ENDPOINTS.accounts.me)
  return unwrapEnvelope(response.data)
}
