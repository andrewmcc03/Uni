<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Arr;
use App\Models\Job;

Route::get('/', function () {
    return view('home', ['greeting' => 'Hello', 'name' => 'Andrew']);
});

// Index
Route::get('/jobs', function () {
    $jobs = Job::with('employer')->latest()->paginate(3);

    return view('jobs.index', [
        'jobs' => $jobs
    ]);
});

// Create
Route::get('/jobs/create', function () {
    return view('jobs.create');
});

// Show
Route::get('/jobs/{id}', function ($id) {
    $job = Job::find($id);

    return view('jobs.show', ['job' => $job]);
});

// Store
Route::post('/jobs', function () {
    // Validation here ...
    request()->validate([
        'title' => ['required', 'min:3'],
        'salary' => ['required'],
    ]);

    Job::create([
        'title' => request('title'),
        'salary' => request('salary'),
        'employer_id' => 1,
    ]);

    return redirect('/jobs');
});

// Edit
Route::get('/jobs/{id}/edit', function ($id) {
    $job = Job::find($id);

    return view('jobs.edit', ['job' => $job]);
});

// Update
Route::patch('/jobs/{id}', function ($id) {
    // Validate
    request()->validate([
        'title' => ['required', 'min:3'],
        'salary' => ['required']
    ]);

    // Authorise (on hold ...)

    // Update job
    $job = Job::findOrFail($id);

    $job->update([
        'title' => request('title'),
        'salary' => request('salary'),
    ]);
    // Persist

    // Redirect to job page
    return redirect('jobs/' . $job->id);
});

// Destroy (delete)
Route::delete('/jobs/{id}', function ($id) {
    // Authorise (on hold ...)

    // Delete job
    Job::findOrFail($id)->delete();

    // Redirect
    return redirect('/jobs');
});

Route::get('/about', function () {
    return view('about');
});

Route::get('/contact', function () {
    return view('contact');
});
