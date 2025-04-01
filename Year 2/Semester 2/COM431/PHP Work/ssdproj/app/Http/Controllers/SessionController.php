<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\ValidationException;

class SessionController extends Controller
{
    public function create() {
        return view('auth.login');
    }

    public function store() {
        // Validate
        $attributes = request()->validate([
            'email' => ['required', 'email'],
            'password' => ['required']
        ]);

        // Attempt to login user
        if (!Auth::attempt($attributes)) {
            throw ValidationException::withMessages([
                'email' => 'The provided credentials do not match.'
            ]);
        };

        // Regenerate session token
        request()->session()->regenerate();

        // Redirect
        return redirect('/jobs');
    }

    public function destroy() {
        Auth::logout();

        return redirect('/');
    }
}
