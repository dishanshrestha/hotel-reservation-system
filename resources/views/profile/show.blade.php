<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>My Profile - HotelReservation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .profile-container {
            max-width: 600px;
            margin: 40px auto;
        }
        .card {
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-radius: 8px;
            margin-bottom: 25px;
            border: 1px solid #e0e0e0;
        }
        .card-header {
            background: #f8f9fa;
            border-radius: 8px 8px 0 0 !important;
            padding: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        .card-header h3 {
            font-size: 20px;
            font-weight: 700;
            margin: 0;
            color: #333;
        }
        .form-label {
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        .form-control, .form-control:focus {
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 10px 12px;
        }
        .form-control:focus {
            border-color: #333;
            box-shadow: 0 0 0 3px rgba(51, 51, 51, 0.1);
        }
        .btn {
            border-radius: 6px;
            font-weight: 600;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: #333;
            border: none;
            color: white;
        }
        .btn-primary:hover {
            background: #555;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(51, 51, 51, 0.2);
            color: white;
        }
        .btn-secondary {
            background-color: #6c757d;
        }
        .btn-secondary:hover {
            background-color: #5a6268;
            transform: translateY(-2px);
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .btn-danger:hover {
            background-color: #c82333;
            transform: translateY(-2px);
        }
        .btn-group-custom {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .alert {
            border: none;
            border-radius: 6px;
        }
        .profile-photo-preview {
            width: 100px;
            height: 100px;
            border-radius: 8px;
            object-fit: cover;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-top: 10px;
        }
        .section-title {
            font-size: 16px;
            font-weight: 700;
            color: #333;
            margin-top: 25px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }
        .nav-link-back {
            color: #333;
            text-decoration: none;
            font-weight: 600;
            margin-bottom: 20px;
            display: inline-block;
        }
        .nav-link-back:hover {
            color: #666;
        }
    </style>
</head>
<body>
    @include('home.header')

    <div class="profile-container">
        <a href="{{ url('/') }}" class="nav-link-back">
            <i class="fas fa-arrow-left mr-2"></i>Back to Home
        </a>

        @if(session('message'))
            <div class="alert alert-success alert-dismissible fade show">
                <i class="fas fa-check-circle mr-2"></i>{{ session('message') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        @endif

        @if($errors->any())
            <div class="alert alert-danger alert-dismissible fade show">
                <i class="fas fa-exclamation-circle mr-2"></i>
                <ul class="mb-0">
                    @foreach($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        @endif

        <!-- Profile Information Card -->
        <div class="card">
            <div class="card-header">
                <h3><i class="fas fa-user-circle mr-2"></i>Profile Information</h3>
            </div>
            <div class="card-body">
                <form method="POST" action="{{ route('profile.update') }}" enctype="multipart/form-data">
                    @csrf

                    <div class="mb-3">
                        <label class="form-label"><i class="fas fa-user mr-2"></i>Full Name</label>
                        <input type="text" name="name" class="form-control @error('name') is-invalid @enderror" value="{{ old('name', $user->name) }}" required>
                        @error('name')<span class="invalid-feedback">{{ $message }}</span>@enderror
                    </div>

                    <div class="mb-3">
                        <label class="form-label"><i class="fas fa-envelope mr-2"></i>Email Address</label>
                        <input type="email" name="email" class="form-control @error('email') is-invalid @enderror" value="{{ old('email', $user->email) }}" required>
                        @error('email')<span class="invalid-feedback">{{ $message }}</span>@enderror
                    </div>

                    <div class="mb-3">
                        <label class="form-label"><i class="fas fa-phone mr-2"></i>Phone Number</label>
                        <input type="text" name="phone" class="form-control @error('phone') is-invalid @enderror" value="{{ old('phone', $user->phone ?? '') }}" placeholder="Optional">
                        @error('phone')<span class="invalid-feedback">{{ $message }}</span>@enderror
                    </div>

                    <div class="section-title">Profile Photo</div>
                    <div class="mb-3">
                        <input type="file" name="profile_photo" class="form-control @error('profile_photo') is-invalid @enderror" accept="image/*">
                        @error('profile_photo')<span class="invalid-feedback">{{ $message }}</span>@enderror
                        @if($user->profile_photo_path)
                            <div class="mt-3">
                                <small class="text-muted">Current Photo:</small>
                                <br>
                                <img src="{{ asset('storage/'.$user->profile_photo_path) }}" alt="avatar" class="profile-photo-preview" />
                            </div>
                        @endif
                    </div>

                    <div class="btn-group-custom">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save mr-2"></i>Save Changes
                        </button>
                        <a href="{{ route('settings') }}" class="btn btn-secondary">
                            <i class="fas fa-cog mr-2"></i>Account Settings
                        </a>
                    </div>
                </form>
            </div>
        </div>

        <!-- Change Password Card -->
        <div class="card">
            <div class="card-header">
                <h3><i class="fas fa-lock mr-2"></i>Change Password</h3>
            </div>
            <div class="card-body">
                <form method="POST" action="{{ route('profile.update-password') }}">
                    @csrf

                    <div class="mb-3">
                        <label class="form-label"><i class="fas fa-lock mr-2"></i>Current Password</label>
                        <input type="password" name="current_password" class="form-control @error('current_password') is-invalid @enderror" required>
                        @error('current_password')<span class="invalid-feedback">{{ $message }}</span>@enderror
                    </div>

                    <div class="mb-3">
                        <label class="form-label"><i class="fas fa-key mr-2"></i>New Password</label>
                        <input type="password" name="password" class="form-control @error('password') is-invalid @enderror" required>
                        @error('password')<span class="invalid-feedback">{{ $message }}</span>@enderror
                        <small class="text-muted d-block mt-1">
                            <i class="fas fa-info-circle mr-1"></i>Must be at least 8 characters
                        </small>
                    </div>

                    <div class="mb-3">
                        <label class="form-label"><i class="fas fa-check-circle mr-2"></i>Confirm Password</label>
                        <input type="password" name="password_confirmation" class="form-control @error('password_confirmation') is-invalid @enderror" required>
                        @error('password_confirmation')<span class="invalid-feedback">{{ $message }}</span>@enderror
                    </div>

                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-refresh mr-2"></i>Update Password
                    </button>
                </form>
            </div>
        </div>

        <!-- Account Actions Card -->
        <div class="card">
            <div class="card-header">
                <h3><i class="fas fa-sliders-h mr-2"></i>Account Actions</h3>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <p class="text-muted mb-2"><small>View your booking history and manage reservations</small></p>
                    <a href="{{ url('/mybooking') }}" class="btn btn-primary w-100">
                        <i class="fas fa-calendar-check mr-2"></i>My Bookings
                    </a>
                </div>

                <div class="mb-3">
                    <p class="text-muted mb-2"><small>Sign out from all sessions</small></p>
                    <form method="POST" action="{{ route('logout') }}" style="display: inline;">
                        @csrf
                        <button type="submit" class="btn btn-danger w-100">
                            <i class="fas fa-sign-out-alt mr-2"></i>Logout
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
