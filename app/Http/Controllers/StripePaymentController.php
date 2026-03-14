<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Stripe\Stripe;
use Stripe\Checkout\Session as StripeSession;
use Illuminate\Support\Facades\DB;

class StripePaymentController extends Controller
{
    public function showBookingForm($roomId)
{
    // Fetch room details by ID
    $room = DB::table('rooms')->where('id', $roomId)->first();

    // Check if room exists
    if (!$room) {
        return redirect()->back()->with('error', 'Room not found');
    }

    // Pass room data to the view
    return view('booking_form', ['room' => $room]);
}

public function checkout(Request $request)
{
    // Get the form data
    $name = $request->input('name');
    $email = $request->input('email');
    $phone = $request->input('phone');
    $startDate = $request->input('startDate');
    $endDate = $request->input('endDate');
    $totalPrice = $request->input('total_price');
    $roomId = $request->input('room_id'); // Assuming you have room_id in the form

    // Validate the form data
    $request->validate([
        'name' => 'required|string',
        'email' => 'required|email',
        'phone' => 'required|numeric',
        'startDate' => 'required|date',
        'endDate' => 'required|date|after:startDate',
        'total_price' => 'required|numeric',
        'room_id' => 'required|integer'
    ]);

    // Check if the room is already booked for the given dates
    $isBooked = DB::table('bookings')
        ->where('room_id', $roomId)
        ->where('start_date', '<=', $endDate)
        ->where('end_date', '>=', $startDate)
        ->exists();

    if ($isBooked) {
        return redirect()->back()->with('message', 'Room is already booked for the selected dates. Please try different dates.');
    }

    // Save the booking details in the session (or alternatively use a database for incomplete bookings)
    session([
        'name' => $name,
        'email' => $email,
        'phone' => $phone,
        'startDate' => $startDate,
        'endDate' => $endDate,
        'totalPrice' => $totalPrice,
        'roomId' => $roomId
    ]);

    // Initialize the line items array
    $lineItems = [[
        'price_data' => [
            'currency' => 'usd',
            'product_data' => [
                'name' => "🏨 Booking: {$name}\n📅 Dates: {$startDate} to {$endDate}\n💵 Total: \${$totalPrice}",
            ],
            'unit_amount' => $totalPrice * 100, // Convert dollars to cents
        ],
        'quantity' => 1,
    ]];

    try {
        // Set your Stripe secret key from the environment variable
        Stripe::setApiKey(env('STRIPE_SECRET'));

        // Create a new Stripe Checkout session
        $session = StripeSession::create([
            'payment_method_types' => ['card'],
            'line_items' => $lineItems,
            'mode' => 'payment',
            'success_url' => url('/success'),
            'cancel_url' => url('/cancel'),
        ]);

        // Redirect the user to the Stripe Checkout page
        return redirect()->away($session->url);
    } catch (\Exception $e) {
        // Return error response if something goes wrong
        return response()->json(['error' => $e->getMessage()], 500);
    }
}


    public function success(Request $request)
    {
        // Retrieve booking details from session
        $name = session('name');
        $email = session('email');
        $phone = session('phone');
        $startDate = session('startDate');
        $endDate = session('endDate');
        $totalPrice = session('totalPrice');
        $roomId = session('roomId');

        // Insert the booking record into the database
        DB::table('bookings')->insert([
            'room_id' => $roomId,
            'name' => $name,
            'email' => $email,
            'phone' => $phone,
            'start_date' => $startDate,
            'end_date' => $endDate,
            'total_price' => $totalPrice,
            'status' => 'paid', // Set status as 'paid'
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        // Show success page with SweetAlert
        return view('success');
    }

    public function cancel()
    {
        return "Cancelled";
    }
}
