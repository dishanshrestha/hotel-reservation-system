import { Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import PublicLayout from './components/layout/PublicLayout';
import AdminLayout from './components/layout/AdminLayout';
import AdminRoute from './routes/AdminRoute';

// Public pages
import HomePage from './pages/public/HomePage';
import AboutPage from './pages/public/AboutPage';
import RoomsPage from './pages/public/RoomsPage';
import GalleryPage from './pages/public/GalleryPage';
import BlogPage from './pages/public/BlogPage';
import ContactPage from './pages/public/ContactPage';

// Admin pages
import AdminLoginPage from './pages/admin/LoginPage';
import DashboardPage from './pages/admin/DashboardPage';

function App() {
  return (
    <AuthProvider>
      <Toaster position="top-right" />
      <Routes>
        {/* Public routes */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/rooms" element={<RoomsPage />} />
          <Route path="/gallery" element={<GalleryPage />} />
          <Route path="/blog" element={<BlogPage />} />
          <Route path="/contact" element={<ContactPage />} />
        </Route>

        {/* Admin login (no layout) */}
        <Route path="/admin/login" element={<AdminLoginPage />} />

        {/* Admin protected routes */}
        <Route
          element={
            <AdminRoute>
              <AdminLayout />
            </AdminRoute>
          }
        >
          <Route path="/admin" element={<DashboardPage />} />
        </Route>

        {/* 404 */}
        <Route
          path="*"
          element={
            <div className="min-h-screen flex items-center justify-center">
              <div className="text-center">
                <h1 className="text-6xl font-bold text-brand-primary mb-4">404</h1>
                <p className="text-xl text-gray-600 mb-6">Page not found</p>
                <a href="/" className="px-6 py-2 bg-brand-primary text-white rounded-md hover:bg-brand-primary-dark">
                  Go Home
                </a>
              </div>
            </div>
          }
        />
      </Routes>
    </AuthProvider>
  );
}

export default App;
