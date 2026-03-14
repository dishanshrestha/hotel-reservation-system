<div class="container">
    <h1 class="my-4">Available Rooms</h1>
    <div class="row">
        @forelse($rooms as $room)
        <div class="col-md-4 mb-4">
            <div class="card h-100">
            <figure><img src="/room/{{$room->image}}" alt="Room Image"/></figure>
                <div class="card-body">
                    <h5 class="card-title">{{ $room->type }} Room</h5>
                    <p class="card-text">Price: Rs. {{ number_format($room->price, 2) }} per night</p>
                    <p class="card-text">{{ $room->description }}</p>
                </div>
                <div class="card-footer">
                    <a href="{{url('room_details',$room->id)}}" class="btn btn-primary">View Details</a>
                </div>
            </div>
        </div>
        @empty
        <div class="col-12">
            <p>No rooms available for the selected criteria.</p>
        </div>
        @endforelse
    </div>
</div>
