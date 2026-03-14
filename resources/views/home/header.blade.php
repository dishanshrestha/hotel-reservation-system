<!-- header inner -->
<div class="header">
    <div class="container">
        <div class="row">
            <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col logo_section">
                <div class="full">
                    <div class="center-desk">
                        <div class="logo">
                            <a href="{{ url('/') }}"><img src="images/nepalstay.png" alt="NepalStay Logo" width="150px" height="150px" /></a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-9 col-lg-9 col-md-9 col-sm-9">
                <nav class="navigation navbar navbar-expand-md navbar-dark">
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample04" aria-controls="navbarsExample04" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarsExample04">
                        <ul class="navbar-nav mr-auto">
                            <li class="nav-item {{ request()->is('/') ? 'active' : '' }}">
                                <a class="nav-link" href="{{ url('/') }}">Home</a>
                            </li>
                            <li class="nav-item {{ request()->is('our_rooms') ? 'active' : '' }}">
                                <a class="nav-link" href="{{ url('our_rooms') }}">Rooms</a>
                            </li>
                            <li class="nav-item {{ request()->is('hotel_gallary') ? 'active' : '' }}">
                                <a class="nav-link" href="{{ url('hotel_gallary') }}">Gallery</a>
                            </li>

                            @auth
                            <li class="nav-item {{ request()->is('mybooking') ? 'active' : '' }}">
                                <a class="nav-link" href="{{ url('mybooking') }}">Bookings</a>
                            </li>
                            @endauth

                            <li class="nav-item {{ request()->is('contact_us') ? 'active' : '' }}">
                                <a class="nav-link" href="{{ url('contact_us') }}">Contact</a>
                            </li>
                        </ul>

                        <ul class="navbar-nav ml-auto">
                            @auth
                            <li class="nav-item">
                                <a class="nav-link d-flex align-items-center" href="{{ route('profile.show') }}">
                                    @if(Auth::user()->profile_photo_path)
                                        <img src="{{ asset('storage/' . Auth::user()->profile_photo_path) }}" alt="avatar" style="width:32px;height:32px;border-radius:50%;object-fit:cover;margin-right:8px;" />
                                    @else
                                        <i class="fas fa-user-circle mr-1" style="font-size:22px;margin-right:8px;"></i>
                                    @endif
                                    <span>{{ Auth::user()->name }}</span>
                                </a>
                            </li>
                            <li class="nav-item">
                                <form method="POST" action="{{ route('logout') }}" class="logout-form">
                                    @csrf
                                    <button type="submit" class="btn btn-link nav-link">
                                        <i class="fas fa-sign-out-alt mr-1"></i> Logout
                                    </button>
                                </form>
                            </li>
                            @else
                            <li class="nav-item">
                                <a class="btn btn-success mr-2" href="{{ route('login') }}">
                                    <i class="fas fa-sign-in-alt mr-1"></i> Login
                                </a>
                            </li>
                            @if (Route::has('register'))
                            <li class="nav-item">
                                <a class="btn btn-primary" href="{{ route('register') }}">
                                    <i class="fas fa-user-plus mr-1"></i> Register
                                </a>
                            </li>
                            @endif
                            @endauth
                        </ul>
                    </div>
                </nav>
            </div>
        </div>
    </div>
</div>

<style>
    .header {
        background-color: #343a40;
        padding: 8px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .logo img {
        transition: transform 0.3s ease;
        height: 50px !important;
        width: auto !important;
    }
    
    .logo img:hover {
        transform: scale(1.05);
    }
    
    .navigation {
        padding: 5px 0;
    }
    
    .nav-link {
        font-size: 15px;
        font-weight: 500;
        padding: 6px 12px !important;
        transition: all 0.3s ease;
        color: white !important;
    }
    
    .nav-link:hover {
        color: #17a2b8 !important;
    }
    
    .nav-item.active .nav-link {
        color: #17a2b8 !important;
        font-weight: 600;
    }
    
    .btn-link.nav-link {
        display: inline;
        padding: 6px 12px !important;
        background: transparent;
        border: none;
        outline: none;
    }
    
    .btn-link.nav-link:hover {
        color: #17a2b8 !important;
        text-decoration: none;
    }
    
    .logout-form {
        display: inline;
    }
    
    .navbar-toggler {
        border: none;
    }
    
    .navbar-toggler:focus {
        outline: none;
    }
</style>

<!-- Required JavaScript Libraries -->
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>

<script>
    $(document).ready(function() {
        // Close mobile menu when clicking a link
        $('.navbar-nav>li>a').on('click', function(){
            $('.navbar-collapse').collapse('hide');
        });
    });
</script>