export type Role = 'CUSTOMER' | 'SELLER';

export interface ApiEnvelope<T> {
  success: boolean;
  message: string;
  data: T;
  errors: unknown;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  sku: string;
  price: string;
  stock: number;
  is_active: boolean;
}

export interface Order {
  id: number;
  status: 'PENDING' | 'CONFIRMED' | 'REJECTED';
  total_amount: string;
  rejection_reason: string;
  created_at: string;
}
