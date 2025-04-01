<?php

namespace App\Http\Controllers;

use App\Models\Job;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Gate;

class JobController extends Controller
{
    // Index
    public function index() {
        $jobs = Job::with('employer')->latest()->paginate(3);

        return view('jobs.index', [
            'jobs' => $jobs
        ]);
    }

    // Create
    public function create() {
        return view('jobs.create');
    }

    // Show
    public function show(Job $job) {
        return view('jobs.show', ['job' => $job]);
    }

    // Store
    public function store() {
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
    }

    // Edit
    public function edit(Job $job) {
        return view('jobs.edit', ['job' => $job]);
    }

    // Update
    public function update(Job $job) {
        // Authorise (on hold ...)

        // Validate
        request()->validate([
            'title' => ['required', 'min:3'],
            'salary' => ['required']
        ]);

        // Update job
        $job->update([
            'title' => request('title'),
            'salary' => request('salary'),
        ]);
        // Persist

        // Redirect to job page
        return redirect('jobs/' . $job->id);
    }

    // Destroy (delete)
    public function destroy(Job $job) {
        // Authorise (on hold ...)

        // Delete job
        $job->delete();

        // Redirect
        return redirect('/jobs');
    }
}
