<!DOCTYPE html>
<html lang="en">
<head>
    @include('home.css')
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .booking-container {
            background: #f8f9fa;
            padding: 40px 0;
            min-height: 100vh;
        }
        
        .booking-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 30px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e0e0e0;
        }
        
        .booking-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }
        
        .booking-header {
            background: #f8f9fa;
            color: #333;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .booking-id {
            font-size: 14px;
            opacity: 0.7;
        }
        
        .status-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-pending {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .status-approved {
            background-color: #d4edda;
            color: #155724;
        }
        
        .status-rejected {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .status-canceled {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .booking-body {
            padding: 25px;
        }
        
        .room-info {
            display: flex;
            gap: 25px;
            margin-bottom: 25px;
        }
        
        .room-image {
            width: 200px;
            height: 150px;
            border-radius: 8px;
            object-fit: cover;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .room-details {
            flex: 1;
        }
        
        .room-title {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-bottom: 8px;
        }
        
        .room-type {
            display: inline-block;
            background-color: #e7f3ff;
            color: #0066cc;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 12px;
        }
        
        .room-info-row {
            display: flex;
            gap: 30px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        
        .info-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .info-item i {
            color: #667eea;
            font-size: 16px;
        }
        
        .info-label {
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
        }
        
        .info-value {
            font-size: 16px;
            color: #333;
            font-weight: 500;
        }
        
        .timeline {
            margin-top: 25px;
            padding-top: 25px;
            border-top: 2px solid #f0f0f0;
        }
        
        .timeline-title {
            font-weight: 700;
            color: #333;
            margin-bottom: 15px;
            font-size: 14px;
            text-transform: uppercase;
        }
        
        .timeline-item {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            position: relative;
            padding-left: 30px;
        }
        
        .timeline-marker {
            position: absolute;
            left: 0;
            top: 0;
            width: 20px;
            height: 20px;
            background: #667eea;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 0 0 2px #667eea;
        }
        
        .timeline-item.completed .timeline-marker {
            background: #28a745;
            box-shadow: 0 0 0 2px #28a745;
        }
        
        .timeline-item.pending .timeline-marker {
            background: #ffc107;
            box-shadow: 0 0 0 2px #ffc107;
        }
        
        .timeline-item.rejected .timeline-marker {
            background: #dc3545;
            box-shadow: 0 0 0 2px #dc3545;
        }
        
        .timeline-label {
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }
        
        .timeline-date {
            font-size: 12px;
            color: #999;
        }
        
        .price-section {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .price-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        
        .price-label {
            font-weight: 600;
            color: #666;
        }
        
        .price-value {
            font-weight: 700;
            color: #333;
        }
        
        .total-price {
            border-top: 2px solid #ddd;
            padding-top: 10px;
            margin-top: 10px;
            font-size: 18px;
            color: #667eea;
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .btn-cancel {
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-cancel:hover {
            background-color: #c82333;
            transform: translateY(-2px);
        }
        
        .btn-cancel:disabled {
            background-color: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-details {
            background-color: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        
        .btn-details:hover {
            background-color: #5568d3;
            transform: translateY(-2px);
            color: white;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        
        .empty-state i {
            font-size: 64px;
            margin-bottom: 20px;
            opacity: 0.5;
            color: #999;
        }
        
        .empty-state h2 {
            font-size: 28px;
            margin-bottom: 10px;
            color: #333;
        }
        
        .empty-state p {
            font-size: 16px;
            opacity: 0.7;
            color: #666;
        }
        
        .page-title {
            color: #333;
            font-weight: 700;
            margin-bottom: 30px;
            font-size: 32px;
        }
        
        .filter-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            background-color: white;
            color: #333;
            border: 2px solid #e0e0e0;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .filter-btn:hover, .filter-btn.active {
            background-color: #333;
            color: white;
            border-color: #333;
        }
        
        .nights-count {
            background: #f0f0f0;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body class="main-layout">
    <div class="loader_bg">
        <div class="loader"><img src="images/loading.gif" alt="#"/></div>
    </div>
    
    <header>
        @include('home.header')
    </header>

    <div class="booking-container">
        <div class="container">
            <h1 class="page-title">
                <i class="fas fa-calendar-check mr-2"></i>Booking Tracker
            </h1>

            @if(empty($datas) || count($datas) == 0)
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <h2>No Bookings Yet</h2>
                    <p>You haven't made any room bookings. Start exploring our rooms and make your first booking!</p>
                    <a href="{{ url('our_rooms') }}" class="btn btn-light mt-3">Browse Rooms</a>
                </div>
            @else
                <div class="filter-tabs">
                    <button class="filter-btn active" onclick="filterBookings('all')">All Bookings</button>
                    <button class="filter-btn" onclick="filterBookings('approved')">Approved</button>
                    <button class="filter-btn" onclick="filterBookings('pending')">Pending</button>
                    <button class="filter-btn" onclick="filterBookings('cancelled')">Cancelled</button>
                </div>

                @foreach ($datas as $data)
                    @php
                        $statusClass = strtolower(str_replace(' ', '-', $data->status));
                        $daysCount = \Carbon\Carbon::parse($data->start_date)->diffInDays(\Carbon\Carbon::parse($data->end_date));
                    @endphp
                    <div class="booking-card" data-status="{{ $data->status }}">
                        <div class="booking-header">
                            <div>
                                <h3 style="margin: 0; font-size: 18px; font-weight: 700;">Booking #{{ $data->id }}</h3>
                                <p class="booking-id">
                                    <i class="fas fa-calendar-alt"></i>
                                    Booked on {{ \Carbon\Carbon::parse($data->created_at)->format('M d, Y') }}
                                </p>
                            </div>
                            <span class="status-badge status-{{ $statusClass }}">
                                @if($data->status == 'paid')
                                    <i class="fas fa-check-circle"></i> Approved
                                @elseif($data->status == 'waiting')
                                    <i class="fas fa-hourglass-half"></i> Pending
                                @elseif($data->status == 'rejected')
                                    <i class="fas fa-times-circle"></i> Rejected
                                @elseif($data->status == 'Canceled')
                                    <i class="fas fa-ban"></i> Cancelled
                                @else
                                    {{ ucfirst($data->status) }}
                                @endif
                            </span>
                        </div>

                        <div class="booking-body">
                            <div class="room-info">
                                @php
                                    $roomImg = $data->room->image;
                                    if (!\Illuminate\Support\Str::startsWith($roomImg, ['http://','https://'])) {
                                        $roomImg = url('/room/'.$roomImg);
                                    }
                                @endphp
                                <img src="{{ $roomImg }}" alt="{{ $data->room->room_title }}" class="room-image">
                                
                                <div class="room-details">
                                    <h2 class="room-title">{{ $data->room->room_title }}</h2>
                                    <span class="room-type">{{ strtoupper($data->room->room_type) }}</span>
                                    
                                    <div class="room-info-row">
                                        <div class="info-item">
                                            <i class="fas fa-user"></i>
                                            <div>
                                                <div class="info-label">Guest Name</div>
                                                <div class="info-value">{{ $data->name }}</div>
                                            </div>
                                        </div>
                                        <div class="info-item">
                                            <i class="fas fa-envelope"></i>
                                            <div>
                                                <div class="info-label">Email</div>
                                                <div class="info-value">{{ $data->email }}</div>
                                            </div>
                                        </div>
                                        <div class="info-item">
                                            <i class="fas fa-phone"></i>
                                            <div>
                                                <div class="info-label">Phone</div>
                                                <div class="info-value">{{ $data->phone ?? 'N/A' }}</div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="room-info-row">
                                        <div class="info-item">
                                            <i class="fas fa-sign-in-alt"></i>
                                            <div>
                                                <div class="info-label">Check-in</div>
                                                <div class="info-value">{{ \Carbon\Carbon::parse($data->start_date)->format('M d, Y') }}</div>
                                            </div>
                                        </div>
                                        <div class="info-item">
                                            <i class="fas fa-sign-out-alt"></i>
                                            <div>
                                                <div class="info-label">Check-out</div>
                                                <div class="info-value">{{ \Carbon\Carbon::parse($data->end_date)->format('M d, Y') }}</div>
                                            </div>
                                        </div>
                                        <div class="info-item">
                                            <i class="fas fa-moon"></i>
                                            <div>
                                                <div class="info-label">Duration</div>
                                                <div class="info-value"><span class="nights-count">{{ $daysCount }} Night{{ $daysCount != 1 ? 's' : '' }}</span></div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="price-section">
                                        <div class="price-row">
                                            <span class="price-label">Price per night:</span>
                                            <span class="price-value">${{ $data->room->price }}</span>
                                        </div>
                                        <div class="price-row">
                                            <span class="price-label">Number of nights:</span>
                                            <span class="price-value">{{ $daysCount }}</span>
                                        </div>
                                        <div class="price-row total-price">
                                            <span class="price-label">Total Price:</span>
                                            <span class="price-value">${{ $data->total_price ?? ($daysCount * $data->room->price) }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Timeline -->
                            <div class="timeline">
                                <div class="timeline-title">Booking Status Timeline</div>
                                
                                <div class="timeline-item {{ $data->status != 'waiting' ? 'completed' : 'pending' }}">
                                    <div class="timeline-marker"></div>
                                    <div>
                                        <div class="timeline-label">Booking Created</div>
                                        <div class="timeline-date">{{ \Carbon\Carbon::parse($data->created_at)->format('M d, Y \a\t h:i A') }}</div>
                                    </div>
                                </div>

                                <div class="timeline-item {{ $data->status == 'paid' ? 'completed' : ($data->status == 'rejected' ? 'rejected' : 'pending') }}">
                                    <div class="timeline-marker"></div>
                                    <div>
                                        <div class="timeline-label">
                                            @if($data->status == 'paid')
                                                Booking Approved
                                            @elseif($data->status == 'rejected')
                                                Booking Rejected
                                            @else
                                                Awaiting Approval
                                            @endif
                                        </div>
                                        <div class="timeline-date">
                                            @if($data->status == 'paid' || $data->status == 'rejected')
                                                {{ \Carbon\Carbon::parse($data->updated_at)->format('M d, Y \a\t h:i A') }}
                                            @else
                                                Pending
                                            @endif
                                        </div>
                                    </div>
                                </div>

                                <div class="timeline-item {{ $data->status == 'paid' ? 'completed' : 'pending' }}">
                                    <div class="timeline-marker"></div>
                                    <div>
                                        <div class="timeline-label">Check-in Date</div>
                                        <div class="timeline-date">{{ \Carbon\Carbon::parse($data->start_date)->format('M d, Y') }}</div>
                                    </div>
                                </div>
                            </div>

                            <!-- Action Buttons -->
                            <div class="action-buttons">
                                @if($data->status != 'Canceled' && $data->status != 'rejected')
                                    <a href="{{ url('cancel_book', $data->id) }}" class="btn-cancel" onclick="return confirm('Are you sure you want to cancel this booking?');">
                                        <i class="fas fa-trash-alt"></i> Cancel Booking
                                    </a>
                                @else
                                    <button class="btn-cancel" disabled>
                                        <i class="fas fa-ban"></i> {{ $data->status == 'Canceled' ? 'Cancelled' : 'Rejected' }}
                                    </button>
                                @endif
                                <a href="{{ url('room_details', $data->room->id) }}" class="btn-details">
                                    <i class="fas fa-door-open"></i> View Room
                                </a>
                                <button type="button" class="btn-details" onclick="window.print();" style="background-color: #6c757d;">
                                    <i class="fas fa-print"></i> Print Booking
                                </button>
                            </div>
                        </div>
                    </div>
                @endforeach
            @endif
        </div>
    </div>

    @include('home.footer')

    <script>
        function filterBookings(status) {
            const cards = document.querySelectorAll('.booking-card');
            const buttons = document.querySelectorAll('.filter-btn');

            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            cards.forEach(card => {
                if (status === 'all') {
                    card.style.display = 'block';
                } else if (status === 'approved' && (card.dataset.status === 'paid' || card.dataset.status === 'Approved')) {
                    card.style.display = 'block';
                } else if (status === 'pending' && card.dataset.status === 'waiting') {
                    card.style.display = 'block';
                } else if (status === 'cancelled' && (card.dataset.status === 'Canceled' || card.dataset.status === 'canceled')) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
