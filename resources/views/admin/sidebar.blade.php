<div class="d-flex align-items-stretch">
      <!-- Sidebar Navigation-->
      <nav id="sidebar">
        <!-- Sidebar Header-->
        <div class="sidebar-header d-flex align-items-center">
          <div class="avatar"><img src="admin/img/balen.jfif" alt="..." class="img-fluid rounded-circle"></div>
          <div class="title">
            <h1 class="h5">Balen City</h1>
            <p>Kathmandu</p>
          </div>
        </div>
        <!-- Sidebar Navidation Menus-->
        <ul class="list-unstyled">
                <li class="{{ request()->is('home') ? 'active' : '' }}"><a href="{{url('home')}}"> <i class="fas fa-home"></i>Home </a></li>
                
                <li><a href="{{url('create_room')}}"><i class="fas fa-plus-circle"></i> Add Rooms</a></li>
                <li><a href="{{url('view_room')}}"><i class="fas fa-eye"></i> View Rooms</a></li>                  
                
              </li>
                <li class="{{ request()->is('bookings') ? 'active' : '' }}">
                  <a href="{{url('bookings')}}"> <i class="fas fa-check-circle"></i>Booking </a>
                </li>
                <li class="{{ request()->is('manage_user') ? 'active' : '' }}">
                  <a href="{{url('manage_user')}}"> <i class="fas fa-user"></i>Manage User </a>
                </li>
                <li class="{{ request()->is('view_gallary') ? 'active' : '' }}">
                  <a href="{{url('view_gallary')}}"> <i class="fas fa-images"></i>Gallery </a>
                </li>
                <li class="{{ request()->is('all_messages') ? 'active' : '' }}">
                  <a href="{{url('all_messages')}}"> <i class="fas fa-envelope"></i>Messages </a>
                </li>
        </ul>
      </nav>