import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Businesses } from './components/businesses/businesses';

@Component({
  imports: [RouterOutlet, Businesses],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  protected readonly title = signal('bizFE');
}
