import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import { AuthProvider, useAuth } from './auth';
import { LoginPage, MyOrdersPage, ProductListPage, SellerPanelPage } from './pages';

function Protected({ children }: { children: React.ReactNode }) {
  const { auth } = useAuth();
  if (!auth.access) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function SellerProtected({ children }: { children: React.ReactNode }) {
  const { auth } = useAuth();
  if (!auth.access) return <Navigate to="/login" replace />;
  if (auth.role !== 'SELLER') return <Navigate to="/" replace />;
  return <>{children}</>;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<ProductListPage />} />
      <Route
        path="/orders"
        element={
          <Protected>
            <MyOrdersPage />
          </Protected>
        }
      />
      <Route
        path="/seller"
        element={
          <SellerProtected>
            <SellerPanelPage />
          </SellerProtected>
        }
      />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <h1>Aarambha Store</h1>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}
