export const API_ENDPOINTS = {
  accounts: {
    register: '/accounts/register/',
    login: '/accounts/login/',
    refresh: '/accounts/refresh/',
    me: '/accounts/me/',
  },
  catalog: {
    products: '/catalog/products/',
    productDetail: (id: string | number) => `/catalog/products/${id}/`,
    categories: '/catalog/categories/',
  },
  cart: {
    me: '/cart/me/',
    items: '/cart/items/',
    itemById: (id: string | number) => `/cart/${id}/items/`,
  },
  orders: {
    checkout: '/orders/checkout/',
    myOrders: '/orders/my-orders/',
    myOrderById: (id: string | number) => `/orders/${id}/my-order/`,
  },
  promotions: {
    validateCode: '/promotions/codes/validate/',
  },
  shipping: {
    calculate: '/shipping/configs/calculate/',
    active: '/shipping/configs/active/',
  },
} as const
