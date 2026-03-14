<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;
use App\Models\Room;

class RoomRatingProvider extends ServiceProvider
{
    public function boot()
    {
        View::composer(['home.room_details', 'home.room'], function ($view) {
            $id = request()->route('id'); // Get the room ID from the request or route
            $room = Room::withCount('room_ratings')
                        ->withSum('room_ratings', 'rating')
                        ->find($id);

            $avgRating = '0.00';
            $avgRatingPer = 0;
            if ($room && $room->room_ratings_count > 0) {
                $avgRating = number_format($room->room_ratings_sum_rating / $room->room_ratings_count, 2);
                $avgRatingPer = ($avgRating * 100) / 5;
            }

            $view->with(compact('room', 'avgRating', 'avgRatingPer'));
        });
    }
}
