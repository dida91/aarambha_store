export interface Category {
  id: number
  name: string
  slug: string
  description: string
  is_active: boolean
}

export interface ProductImage {
  id: number
  image: string | { url?: string } | null
  alt_text: string
  is_primary: boolean
}

export interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: string
  stock_quantity: number
  is_active: boolean
  category: number
  category_name: string
  images: ProductImage[]
  created_at: string
  updated_at: string
}
