<x-layout>
    <x-slot:heading>Job Listings Page</x-slot:heading>

    <h2 class="font-bold text-lg">{{ $job->title }}</h2>

    <p>This job pays {{ $job->salary }}/year.</p>

    @can('edit', $job)
        <p class="mt-6">
            <x-button href="/jobs/{{ $job->id }}/edit">Edit Job</x-button>
        </p>
    @endcan
</x-layout>
