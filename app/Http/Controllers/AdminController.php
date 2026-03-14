<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use App\Models\Room;
use App\Models\Booking;
use App\Models\Gallary;
use App\Models\Contact;
use App\Notifications\SendEmailNotification;
use Notification;
use DB;




class AdminController extends Controller
{
    public function index()
    {

        if (Auth::id())  //this mean if some one is tries to login
        {
            $usertype = Auth()->user()->usertype;

            if ($usertype == 'user') {
                $room = Room::all();

                $gallery = Gallary::all();

                return view('home.index', compact('room', 'gallery'));
            } else if ($usertype == 'admin') {
                //For Chart
                $bookings = Booking::selectRaw('MONTH(created_at) as month, COUNT(*) as count')
                    ->whereYear('created_at', date('Y'))
                    ->groupBy('month')
                    ->orderBy('month')
                    ->get();
                $labels = [];
                $data = [];
                $colors = ['#FF6384', '#36A2EB', '#FFCE56', '#8BC34A', '#FF5722', '#009688', '#795548', '#9C27B0', '#2196F3', '#FF9800', '#CDDC39', '#607D8B'];

                for ($i = 1; $i <= 12; $i++) {
                    $month = date('F', mktime(0, 0, 0, $i, 1));
                    $count = 0;

                    foreach ($bookings as $booking) {
                        if ($booking->month == $i) {
                            $count = $booking->count;
                            break;
                        }
                    }
                    array_push($labels, $month);
                    array_push($data, $count);
                }

                $datasets = [
                    [
                        'label' => 'Bookings',
                        'data' => $data,
                        'backgroundColor' => $colors
                    ]
                ];
                
                 // Count the number of bookings for each status
                $rejectedCount = Booking::where('status', 'rejected')->count();
                $canceledCount = Booking::where('status', 'canceled')->count();
                $approvedCount = Booking::where('status', 'paid')->count();
                $waitingCount = Booking::where('status', 'waiting')->count();


                // Get the total number of users
                $totalUsers = User::count();
                $totalBookings = Booking::count();
                $totalRoom = Room::count();
                $totalIncome = Booking::sum('total_price');
                return view('admin.index', compact('totalUsers', 'totalBookings', 'totalRoom', 'totalIncome', 'datasets', 'labels','rejectedCount', 'canceledCount', 'approvedCount','waitingCount'));
            } else {
                return redirect()->back();
            }
        }

    }

    public function home()
    {

        $room = Room::all();

        $gallery = Gallary::all();

        return view('home.index', compact('room', 'gallery'));
    }

    public function create_room()
    {
        return view('admin.create_room');
    }

    //inserting the Data to DB
    public function add_room(Request $request)
    {

        $data = new Room;

        $data->room_title = $request->title;  //Here room_title is a field_name in DB and title is name of form
        $data->description = $request->description;

        $data->price = $request->price;

        $data->wifi = $request->wifi;

        $data->room_type = $request->type;

        $image = $request->image;  //get image from form

        if ($image) {

            $imagename = time() . '.' . $image->getClientOriginalExtension();  //modify the image name using time function

            $request->image->move('room', $imagename);  //moving the image in public folder with certain name

            $data->image = $imagename;   //storing the data in DB
        }

        $data->save();

        return redirect()->back();

    }

    //Displaying the room
    public function view_room()
    {
        $datas = Room::all();   //here 'Room' is modal name and all data from table is store in $data variable

        return view('admin.view_room', compact('datas'));  //all the data from $data is send to blade file
    }

    //Deleting the room
    public function room_delete($id)
    {
        $data = Room::find($id);
        $data->delete();
        return redirect()->back();
    }


    public function room_update($id)
    {

        $data = Room::find($id);
        return view('admin.update_room', compact('data'));
    }

    public function edit_room(Request $request, $id)
    {

        $data = Room::find($id);

        $data->room_title = $request->title;

        $data->description = $request->description;

        $data->price = $request->price;

        $data->wifi = $request->wifi;

        $data->room_type = $request->type;

        $image = $request->image;  //get image from form

        if ($image) {

            $imagename = time() . '.' . $image->getClientOriginalExtension();  //modify the image name using time function

            $request->image->move('room', $imagename);  //moving the image in public folder with certain name

            $data->image = $imagename;   //storing the data in DB
        }


        $data->save();

        return redirect()->back();

    }

    public function bookings()
    {
        $datas = Booking::all();
        return view('admin.booking', compact('datas'));
    }

    public function delete_booking($id)
    {
        $data = Booking::find($id);
        $data->delete();
        return redirect()->back();
    }

    public function approve_book($id)
    {

        $booking = Booking::find($id);

        $booking->status = 'approve';

        $booking->save();

        return redirect()->back();

    }
    public function reject_book($id)
    {

        $booking = Booking::find($id);

        $booking->status = 'rejected';

        $booking->save();

        return redirect()->back();

    }
 //Displaying the room
 public function manage_user()
 {
     $datas = User::all();   //here 'User' is modal name and all data from table is store in $data variable

     return view('admin.manage_user', compact('datas'));  //all the data from $data is send to blade file
 }
// Manage User
 //Deleting the room
 public function delete_user($id)
{
    $user = User::find($id);
    if ($user) {
        $user->delete();
        return redirect()->back()->with('message', 'User deleted successfully');
    } else {
        return redirect()->back()->with('error', 'User not found');
    }
}



 
 public function edit_user(Request $request, $id)
{
    // Find the user by ID
    $user = User::find($id);

    // Update user details
    $user->name = $request->name;
    $user->email = $request->email;
    $user->phone = $request->phone;
    $user->usertype = $request->usertype;

    // Update password if provided
    if ($request->filled('password')) {
        // Validate and hash the new password
        $request->validate([
            'password' => 'required|min:8|confirmed',
        ]);
        $user->password = bcrypt($request->password);
    }

    // Save the updated user details
    $user->save();

    // Redirect back to the previous page
    return redirect()->back()->with('success', 'User updated successfully!');
}


    public function view_gallary()
    {

        $gallery = Gallary::all();

        return view('admin.gallary', compact('gallery'));
    }

    public function upload_gallary(Request $request)
    {
        $data = new Gallary;

        $image = $request->image;

        if ($image) {
            $imagename = time() . '.' . $image->getclientOriginalExtension();
            $request->image->move('gallary', $imagename);
            $data->image = $imagename;
            $data->save();
            return redirect()->back();
        }
    }

    public function delete_gallary($id)
    {
        $data = Gallary::find($id);

        $data->delete();

        return redirect()->back();
    }

    public function all_messages()
    {
        $datas = Contact::all();
        return view('admin.all_message', compact('datas'));
    }

    public function send_mail($id)
    {
        $data = Contact::find($id);
        return view('admin.send_mail', compact('data'));
    }

    public function mail(Request $request, $id)
    {
        $data = Contact::find($id);

        $details = [

            'greeting' => $request->greeting,
            'body' => $request->body,
            'action_text' => $request->action_text,
            'action_url' => $request->action_url,
            'endline' => $request->endline,

        ];
        Notification::send($data, new SendEmailNotification($details));
        return redirect()->back();
    }
}