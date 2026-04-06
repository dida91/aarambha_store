import { useEffect, useState } from 'react';

import { getEnveloped, postEnveloped } from './api';
import { useAuth } from './auth';
import type { Order, Product } from './types';

export function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      await login(username, password);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={onSubmit}>
      <h2>Aarambha Store Login</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}

export function ProductListPage() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    getEnveloped<{ results: Product[] } | Product[]>('/catalog/products/').then((data) => {
      if (Array.isArray(data)) {
        setProducts(data);
      } else {
        setProducts(data.results ?? []);
      }
    });
  }, []);

  return (
    <section>
      <h2>Aarambha Store Products</h2>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.name} - NPR {product.price}
          </li>
        ))}
      </ul>
    </section>
  );
}

export function MyOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    getEnveloped<{ results: Order[] } | Order[]>('/orders/me/').then((data) => {
      if (Array.isArray(data)) {
        setOrders(data);
      } else {
        setOrders(data.results ?? []);
      }
    });
  }, []);

  return (
    <section>
      <h2>My Orders</h2>
      <ul>
        {orders.map((order) => (
          <li key={order.id}>
            #{order.id} - {order.status} - NPR {order.total_amount}
            {order.status === 'REJECTED' && order.rejection_reason ? ` (${order.rejection_reason})` : ''}
          </li>
        ))}
      </ul>
    </section>
  );
}

export function SellerPanelPage() {
  const [code, setCode] = useState('AARAMBHA10');

  const createPromo = async () => {
    const now = new Date();
    const end = new Date(now);
    end.setDate(now.getDate() + 7);

    await postEnveloped('/promotions/codes/', {
      code,
      description: 'Seller promo',
      discount_amount: '10.00',
      min_cart_value: '100.00',
      start_at: now.toISOString(),
      end_at: end.toISOString(),
      usage_limit: 0,
      per_user_limit: 1,
      is_public: true,
      is_active: true,
      allowed_users: [],
    });
  };

  return (
    <section>
      <h2>Seller Management</h2>
      <input value={code} onChange={(e) => setCode(e.target.value)} />
      <button onClick={createPromo}>Create Promo</button>
    </section>
  );
}
