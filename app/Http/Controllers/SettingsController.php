<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class SettingsController extends Controller
{
    public function index()
    {
        $user = Auth::user();
        return view('profile.settings', compact('user'));
    }

    public function update(Request $request)
    {
        $user = Auth::user();

        $request->validate([
            'email' => 'required|email|unique:users,email,' . $user->id,
            'phone' => 'nullable|string|max:30',
        ]);

        $user->email = $request->input('email');
        if ($request->has('phone')) {
            $user->phone = $request->input('phone');
        }
        $user->save();

        return redirect()->route('settings')->with('message', 'Settings updated successfully.');
    }
}
