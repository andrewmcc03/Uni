<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Arr;

Route::get('/', function () {
    return view('home', ['greeting' => 'Hello', 'name' => 'Andrew']);
});

Route::get('/jobs', function () {
    return view('jobs', [
        
        'jobs' => [
            [
                'id' => 1,
                'title' => 'Manager',
                'salary' => '$50,000'
            ],
            [
                'id' => 2,
                'title' => 'Engineer',
                'salary' => '$40,000'
            ],
            [
                'id' => 3,
                'title' => 'Technician',
                'salary' => '$32,000'
            ]
        ]
    ]);
});

Route::get('/jobs/{id}', function ($id) {
    $jobs = [
        [
            'id' => 1,
            'title' => 'Manager',
            'salary' => '$50,000'
        ],
        [
            'id' => 2,
            'title' => 'Engineer',
            'salary' => '$40,000'
        ],
        [
            'id' => 3,
            'title' => 'Technician',
            'salary' => '$32,000'
        ]
    ];

    $job = Arr::first($jobs, fn($job) => $job['id'] == $id);

    return view('job', ['job' => $job]);
});

Route::get('/about', function () {
    return view('about');
});

Route::get('/contact', function () {
    return view('contact');
});

//TEST2