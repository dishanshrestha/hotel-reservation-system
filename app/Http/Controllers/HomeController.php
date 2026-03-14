<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Models\Room;

use App\Models\Booking;

use App\Models\Contact;
// use App\Models\ProductRating;
use App\Models\RoomRating;


use App\Models\Gallary;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Validator;


class HomeController extends Controller
{
    // public function room_details($id)
    // {

    //     $room = Room::find($id);
    //     return view('home.room_details', compact('room'));
    // }

        public function room_details($id)
    {
        $room = Room::withCount('room_ratings')
                    ->withSum('room_ratings', 'rating')
                    ->with(['room_ratings'])
                    ->findOrFail($id);

        //Rating Calculation
        // dd($room);
        //"room_ratings_count" => 2
        // "room_ratings_sum_rating" => 10.0
        $avgRating = '0.00';
        $avgRatingPer = 0;
        if($room->room_ratings_count>0){
            $avgRating = number_format(($room->room_ratings_sum_rating/$room->room_ratings_count),2);
            $avgRatingPer = ($avgRating*100)/5;
        }
        return view('home.room_details', compact('room','avgRating','avgRatingPer'));
        }


    public function add_booking(Request $request, $id)
    {

        $request->validate([
            'startDate' => 'required|date',

            'endDate' => 'date|after:startDate',
        ]);

        $data = new Booking;

        $data->room_id = $id;

        // If user is logged in, prefer authenticated name/email
        $data->name = Auth::check() ? Auth::user()->name : $request->input('name');
        $data->email = Auth::check() ? Auth::user()->email : $request->input('email');
        $data->total_price = $request->input('total_price');
        $data->phone = $request->input('phone');

        // Additional validation for booking details
        $request->validate([
            'phone' => 'nullable|string|max:30',
            'total_price' => 'nullable|numeric|min:0'
        ]);

        $startDate = $request->startDate;

        $endDate = $request->endDate;

        $isBooked = Booking::where('room_id', $id)->where('start_date', '<=', $endDate)->where('end_date', '>=', $startDate)->exists();

        if ($isBooked) {
            return redirect()->back()->with('message', 'Room is already booked please try different date');
        } else {
            $data->start_date = $request->startDate;

            $data->end_date = $request->endDate;

            $data->save();

            return redirect()->back()->with('message', 'Room Book Successfully');
        }
    }

    public function contact(Request $request)
    {
        $contact = new Contact;

        $contact->name = $request->name;
        $contact->email = $request->email;
        $contact->phone = $request->phone;
        $contact->message = $request->message;

        $contact->save();

        return redirect()->back()->with('message', 'Message Sent Successfully');

    }
    public function our_rooms()
    {
        $room = Room::all();
        return view('home.our_rooms', compact('room'));
    }
    public function hotel_gallary()
    {
        $gallery = Gallary::all();
        return view('home.hotel_gallary', compact('gallery'));
    }

    public function contact_us()
    {

        return view('home.contact_us');
    }


    public function mybooking()
    {
        //The user() method of the Auth facade returns the currently authenticated user. It returns an instance of the User model (or whichever model you have configured for authentication).

        $userEmail = Auth::user()->email;  //gives you the email address of the logged-in user.
        $datas = Booking::where('email', $userEmail)->with('room')->orderBy('created_at', 'desc')->get(); //This line performs a query on the Booking model to fetch all booking records where the email field matches the authenticated user's email:
        return view('home.booking_tracker', compact('datas'));
    }


    public function cancel_book($id)
    {

        $booking = Booking::find($id);

        $booking->status = 'Canceled';

        $booking->save();

        return redirect()->back();
    }


    //Search
    // public function search(Request $request)
    // {
    //     // Get the input values from the form
    //     $priceRange = $request->input('price_range');
    //     $roomType = $request->input('room_type');

    //     // Start building the query on the Room model
    //     $rooms = Room::query();

    //     // Apply filters based on input values
    //     if ($priceRange) {
    //         [$minPrice, $maxPrice] = explode('-', $priceRange);
    //         $rooms->whereBetween('price', [(int) $minPrice, (int) $maxPrice]);
    //     }

    //     if ($roomType) {
    //         $rooms->where('room_type', $roomType);
    //     }

    //     // Execute the query and get the filtered rooms
    //     $rooms = $rooms->get();

    //     // Return the view with the filtered rooms
    //     return view('home.search_result', compact('rooms'));
    // }
    public function search(Request $request)
{
    // Get the input values from the form
    $priceRange = $request->input('price_range');
    $roomType = $request->input('room_type');

    // Fetch all rooms from the database (consider adding pagination if the dataset is large)
    $allRooms = Room::all();

    // Initialize an empty collection for the results
    $filteredRooms = collect();

    // If price range is provided, split it into min and max price
    $minPrice = $maxPrice = null;
    if ($priceRange) {
        // Handle cases where price_range is not properly formatted
        if (strpos($priceRange, '-') !== false) {
            [$minPrice, $maxPrice] = explode('-', $priceRange);
            $minPrice = (int) $minPrice;
            $maxPrice = (int) $maxPrice;
        }
    }

    // Perform linear search over all rooms
    foreach ($allRooms as $room) {
        $matchesPrice = true;  // Default to true unless we have price filtering
        $matchesType = true;   // Default to true unless we have type filtering

        // Check if the room matches the price range
        if ($minPrice !== null && $maxPrice !== null) {
            $matchesPrice = ($room->price >= $minPrice && $room->price <= $maxPrice);
        }

        // Check if the room matches the room type
        if (!empty($roomType)) {
            $matchesType = ($room->room_type == $roomType);
        }

        // If the room matches both criteria, add it to the filtered results
        if ($matchesPrice && $matchesType) {
            $filteredRooms->push($room);
        }
    }

    // Return the view with the filtered rooms
    return view('home.search_result', ['rooms' => $filteredRooms]);
}


    public function saveRating($id, Request $request){
        $validator = Validator::make($request->all(), [
            'name' => 'required|min:5',
            'email' => 'required|email',
            'comment' => 'required',
            'rating' => 'required|integer|min:1|max:5'
        ]);
    
        if ($validator->fails()) {
            return response()->json([
                'status' => false,
                'errors' => $validator->errors()
            ]);
        }
    
        $count = RoomRating::where('room_id', $id)->where('email', $request->email)->count();
        if ($count > 0) {
            return response()->json([
                'status' => 'duplicate',
                'message' => 'You already rated this Room'
            ]);
        }
    
        $roomRating = new RoomRating;
        $roomRating->room_id = $id;
        $roomRating->username = $request->name;
        $roomRating->email = $request->email;
        $roomRating->comment = $request->comment;
        $roomRating->rating = $request->rating;
        $roomRating->status = 1;
        $roomRating->save();
    
        session()->flash('success', 'Thanks for your rating.');
    
        return response()->json([
            'status' => true,
            'message' => 'Thanks for your rating.'
        ]);
    }
    
    
    
}
