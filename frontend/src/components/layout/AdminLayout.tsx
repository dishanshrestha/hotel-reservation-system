import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LayoutDashboard, LogOut, Home } from 'lucide-react';

export default function AdminLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top bar */}
      <header className="bg-brand-primary text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <LayoutDashboard size={22} />
              <span className="text-lg font-semibold">Admin Dashboard</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-teal-100 hidden sm:inline">
                Welcome, {user?.name}
              </span>
              <Link
                to="/"
                className="flex items-center gap-1 text-sm text-teal-100 hover:text-white transition-colors"
              >
                <Home size={16} />
                <span className="hidden sm:inline">Site</span>
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1 text-sm text-teal-100 hover:text-white transition-colors"
              >
                <LogOut size={16} />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}
