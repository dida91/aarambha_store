export interface ApiEnvelope<T> {
  success: boolean
  message: string
  data: T
  errors: Record<string, string[] | string> | string[] | string | null
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ApiErrorShape {
  message: string
  status: number
  errors: Record<string, string[]>
}
